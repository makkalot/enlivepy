[![Build Status](https://travis-ci.org/makkalot/enlivepy.svg?branch=master)](https://travis-ci.org/makkalot/enlivepy)

Enlivepy
===========

Python port of clojure [enlive library](https://github.com/cgrand/enlive) for html transformation.
It is a simple wrapper over the famous lxml library in Python. When needed, you still can do all
the fun stuff with lxml under the hood. It is not a templating library it is way more powerful than
that :) 


Installation
-----------------

To install the latest stable version :

    pip install enlivepy



Transformation Concept
-----------------------
Enlivepy is built on concept called transformation chaining. The genereal idea is you select some html nodes
with css selection(similar to Jquery) and pass those nodes to a function/class that expects the node(s) as
first argument. As next step, transformation function returns the changed nodes back and the same process can
be applied to the next function which is on the chain. The node parameter passed to transformer function is
instance of lxml.Element. Therefore, you can do everything you do with lxml. However, library users probably
won't need that much low level access to the nodes because, library already has lots of useful transformer functions.

By default selector-transformation pairs are run sequentially. Rules are applied top-down: the first rule transforms the whole tree and the resulting tree is passed to the next rules.

Here is an example of transformation :

```python

	In [3]: from enlivepy.transformers import *

	In [4]: from lxml.html import fromstring

	In [5]: HTML_DIV = """
	   ...:     <title>Some dummy title</title>
	   ...:     <body>
	   ...:         <div class="content">
	   ...:             <b>Some bold text</b>
	   ...:         </div>
	   ...:     </body>
	   ...:     """

	In [9]: node = fromstring(HTML_DIV)
	In [14]: transformed = transform(node, "div.content > b", content("hello"))

	In [15]: emit(transformed)
	Out[15]: '\n<html>\n  <head>\n    <title>Some dummy title</title>\n  </head>\n  <body>\n        <div class="content">\n            <b>hello</b>\n        </div>\n    </body>\n</html>\n'
```



The __transform__ function takes a single node, selector and tranformation function. The transformation used here
is __content__ function. It may seem at first a little bit weird, but content is a function that returns back
another function which expects finally the selected nodes. It is something like :

```python

	def content(*args):
		def _transform(node):
			#do your stuff with node
			return node

		return _transform
```


You can use classes for the same purpose if more comfortable.


Selector Syntax
---------------------

The first step of transformation is to filter out the nodes that are not needed. For that purpose the library is
using (cssselect)[] library which is used inside of lxml. The select function returns back a list of selected nodes
that obey to the css selection, if no node is found an exception is fired. Here are a few examples of css selection:

```python

	from enlivepy.transformers import select

	select(node, "div")
	select(node, "body script")
	select(node, "ul.outline > li, ol.outline > li")
	select(node, "div > *")
```



Concepts
-----------------------

__snippet__ is a unit of your page. It may be logical or visual entry, such as header, footer, page element. Snippet is usually a part of a template, and may serve as a container for other snippets.So, snippets return a sequence of nodes, it can be used as a building block for more complex templates.

__templates__ combine snippets together, they serve like a basement for the snippets. The difference between snippet
and template is : snippets return a portion of the html file (like the form element) but templates return the whole
transformed page back to the user.

Next concept is __selectors__, which are used within snippets and templates to identify the block of HTML code the transformation would be applied to. They’re very similar to CSS selectors, but also allow more sophisticated, predicate-based selections, for example, you can select a tag based on some part of content, or an attribute. Transformations are functions that triggered on the elements found by selectors. They receive content obtained selector, and modify it in some way.


Quickstart Tutorial
===========================

Template
--------------------------

Let's say we have an html base page like this :

```html

	<!DOCTYPE html>
	<html lang="en">
	  <head>
	    <title>This is a title placeholder</title>
	  </head>
	  <body>
	  </body>
	</html>
```


And we want to change the title of the page with our dynamic stuff. We will have to create a new template like :

```python

	from enlivepy.template import StringTemplate
	from enlivepy.transformers import *

	class BaseTemplate(StringTemplate):

	    template = HTML_BASE

	    def transform(self, nodes, *args, **kwargs):
	        at(nodes,
	           "head title", content(kwargs.get("content_text")))

	        return nodes
```


And here is the usage of the template :

```python

	tmpl = BaseTemplate()
	emit(tmpl(content_text="dynamic_text"))

	'\n<html lang="en">\n  <head>\n    <title>dynamic_text</title>\n  </head>\n  <body>\n\t  </body>\n</html>\n'
```



The most important part of a template is its __transform__ method. That is the place where
we query the nodes and transform them. In example above we use __at__ method which is like
__transform__ utility but accepts multiple selector and tranformer functions it is like :

```python

	at(nodes,
	   "select1", transform1,
	   "select2", transform2
	   ...)
```


We can do the same thing with decorators : for those who like the functional way of doing things :

```python

	from enlivepy.template import template_from_str


	@template_from_str(HTML_BASE)
	def base_template(nodes, *args, **kwargs):
	    at(nodes,
	           "head title", content(kwargs.get("content_text")))

	    return nodes

```


And here is the usage of the template :
```python
	
	emit(base_template(content_text="dynamic_text"))
	'\n<html lang="en">\n  <head>\n    <title>dynamic_text</title>\n  </head>\n  <body>\n\t  </body>\n</html>\n'
```



Snippet
-------------------

Let's add several snippets. For example, navigation and some content. For that, let's first define a template for the navigation.

```html

	<!DOCTYPE html>
	<html lang="en">
	  <body>
	    <header>
	      <h1>Header placeholder</h1>
	      <ul id="navigation">
	        <li><a href="#">Placeholder for navigation</a></li>
	      </ul>
	    </header>
	  </body>
	</html>
```


And here is the implementation of Snippet :

```python

	from enlivepy.snippet import StringSnippet

	class NavSnippet(StringSnippet):

	    template = HTML_NAV
	    selection = "header"

	    def transform(self, nodes, *args, **kwargs):
	        at(nodes,
	           "h1", content(kwargs.get("head_content")),
	           "ul > li:first-child", clone_for(kwargs["urls"],
	                                            "li a", lambda u: content(u["caption"]),
	                                            "li a", lambda u: set_attr(href=u["url"])))

	        return nodes


	urls = [
	    {"caption":"Google", "url":"http://google.com"},
	    {"caption":"Amazon", "url":"http://amazon.com"}
	]

```



And here is the usage :

```python

	nav = NavSnippet()
	emit(nav(head_content="snippet_content",
         urls = urls))

    '\n<header><h1>snippet_content</h1>\n\t      <ul id="navigation"><li><a href="http://google.com">Google</a></li>\n\t      <li><a href="http://amazon.com">Amazon</a></li>\n\t      \n\t      </ul></header>\n'

```


The concept is almost similar like Template but we have to supply a selection attribute to select the part we are interested in. As it is seen in the example the result of calling the snippet is __only__ the __header__ part of the
html tree not the whole tree is gathered back.

In this example we used more complex tranformation called __clone_for__ . You can check the wiki for more information about it.


And here is the decorator version of the code above :

```python

	from enlivepy.snippet import snippet_from_str

	@snippet_from_str(HTML_NAV, "header")
	def nav_snippet(nodes, *args, **kwargs):
	    at(nodes,
	           "h1", content(kwargs.get("head_content")),
	           "ul > li:first-child", clone_for(kwargs["urls"],
	                                            "li a", lambda u: content(u["caption"]),
	                                            "li a", lambda u: set_attr(href=u["url"])))

	    return nodes
```


And here is the usage :

```python
	emit(nav_snippet(head_content="snippet_content",
	     urls = urls))

	'\n<header><h1>snippet_content</h1>\n\t      <ul id="navigation"><li><a href="http://google.com">Google</a></li>\n\t      <li><a href="http://amazon.com">Amazon</a></li>\n\t      \n\t      </ul></header>\n'

```


Transformations
----------------------

A transformation is a function that returns either a node or collection of node.

Enlivepy defines several helper functions:


```python
	
	#Replaces the content of the element. Values can be nodes or collection of nodes.
	content("xyz", node_a, "abc")

	#Wraps selected node into the given tag
	wrap("div")
	#or
	wrap("div", {"class":"foo"})

	#Opposite to wrap, returns the content of the selected node
	unwrap

	#Sets given key value pairs as attributes for selected node
	set_attr(**{"attr1": "val1", "attr2": "val2"})
	
	#Removes attribute(s) from selected node
	remove_attr("attr1", "attr2")

	#Adds class(es) to the selected node
	add_class("foo", "bar")
	
	#Removes class(es) from the selected node
	remove_class("foo", "bar")

	#Chains (composes) several transformations. Applies functions from left to right.
	do(transformation1, transformation2)

	#Clones the selected node, applying transformations to it.
	clone_for(items,  transformation)
	
	#or
	clone_for(items,
			  selector1 transformation1
  			  selector2 transformation2)

  	#Appends the values to the content of the selected element.
	append("xyz", a-node, "abc")

	#Prepends the values to the content of the selected element.
	prepend("xyz", a-node, "abc")

	#Inserts the values after the current selection (node or fragment).
	after("xyz", a-node, "abc")

	#Inserts the values before the current selection (node or fragment).
	before("xyz", a-node, "abc")

	#Replaces the current selection (node or fragment).
	substitute("xyz", a-node, "abc")
	
```


Differences from Original Implementation
----------------------

The biggest difference is immutability. In original __enlive__ when you do some transformation
on a node what you get back is a copy of the node. This is an advantage __Clojure__ has because 
of its persistent data structures. We can have similar immutability model on Enlivepy but we need to do __deepcopy__ on every transformation which would have a negative performanve impact.
Other than that we have a few missing peices : 

- move transformations (tobe added)
- beautifu dsl (Python doesn't have macros :| )
- ${vars} subtitution (tobe added)

