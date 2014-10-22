[![Build Status](https://travis-ci.org/makkalot/enlivepy.svg?branch=master)](https://travis-ci.org/makkalot/enlivepy)

Enlivepy
===========

This is a Python port of clojure [enlive library](https://github.com/cgrand/enlive) for html transformation.
It is a simple wrapper over the famous lxml library in Python. If you wish to (or need to), you can still do all the fun stuff with lxml under the hood. I have to note that this is not a templating library - it’s much more powerful and provides you with a far greater variety of opportunities.

Transformation Concept
-----------------------
Enlivepy is built on a concept called transformation chaining. Generally speaking, what you do is selecting some html nodes with CSS selection (pretty similar to how Jquery is) and then passing the nodes to a function or a class that expects the node(s) as first argument.

The next step involves the transformation function returning the changed nodes. The same process can then be applied to the next function waiting on the chain. The node parameter which is passed to this transformer function is an instance of lxml.Element.

This means that in this case you are free to do everything you would normally do with lxml. Keep in mind that library users probably won’t need that much low level access to the nodes. The reason is that the library already contains a huge number of useful transformer functions.

In default state, the selector-transformation pairs are run in a sequential manner. The rules are applied in a hierarchy (top to bottom). The first rule transforms the whole tree and the tree that is a product of that transformation will be passed to the next set of rules.

Here is an example of a transformation :

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



The __transform__ function takes a single node, a selector and a tranformation function. The transformation used here is the __content__ function. I know it might seem a little strange or weird at first, but the content is a function that returns another function. The returned function expects to receive the finally selected nodes. The process is something like this:


```python

	def content(*args):
		def _transform(node):
			#do your stuff with node
			return node

		return _transform
```


If you’re feeling more comfortable with using classes for the some purpose I illustrated, you can do so without any problems (i.e \_\_call\_\_).

Selector Syntax
---------------------

The first step of the transformation is to filter out the nodes that are not needed. For that purpose the library uses (cssselect)[https://pypi.python.org/pypi/cssselect] library which is used inside of lxml. The __select__ function returns a list of selected nodes, all of which obey the CSS selection. In case no node is to be found, an exception will be triggered(done on purpose to catch errors earlier). Here are a few examples of said CSS selection:


```python

	from enlivepy.transformers import select

	select(node, "div")
	select(node, "body script")
	select(node, "ul.outline > li, ol.outline > li")
	select(node, "div > *")
```



Concepts
-----------------------

__snippet__ is a unit of your page. It may be either a logical or a visual entry. Examples include headers, footers or page elements. The snippet is usually a part of a template and may serve as a container for other snippets. Due to snippets returning a sequence of nodes, you can use them to build a block for more complex templates.

__templates__ combine snippets together. You can think of them as a base for the snippets. There is an important difference between the snippet and the template. While snippets return only a portion of the html file (for example the form element), templates return the whole transformed page back to the user.

The next concept I’ll turn my attention to is  __selectors__. The selectors are used within the snippets and templates. Their purpose is to identify the block of HTML code that the transformation will be applied to. You will see that they are very similar to CSS selectors.

Transformations are functions that trigger on elements found by the selectors. When they receive a content obtained selector, they are sure to leave it modified in some way.


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


What we further want to do is change the title of the page with our dynamic stuff. We will have to create a new template like :

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
we put the nodes in a query and transform them. In the example above we used  __at__ method which is like __transform__ utility. The difference is that it accepts multiple selector and tranformer functions. It looks like this :

```python

	at(nodes,
	   "select1", transform1,
	   "select2", transform2
	   ...)
```


We can do the same thing with decorators (for those who like the functional way of doing things) :

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

Let's add several snippets. For example, a navigation one and some content. In order to properly do this, let’s first define a template for the navigation.

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


And here is the implementation of the Snippet :

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



Here is the usage :

```python

	nav = NavSnippet()
	emit(nav(head_content="snippet_content",
         urls = urls))

    '\n<header><h1>snippet_content</h1>\n\t      <ul id="navigation"><li><a href="http://google.com">Google</a></li>\n\t      <li><a href="http://amazon.com">Amazon</a></li>\n\t      \n\t      </ul></header>\n'

```


The concept is really similar to the Template. The difference is that we have to supply a selection attribute to select the part we are interested in. As it can be seen in the example, the result of calling the snippet is __only__ the __header__ part of the html tree. Notice that such process does not gather back the whole tree. 

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


Here you can see the usage :

```python
	emit(nav_snippet(head_content="snippet_content",
	     urls = urls))

	'\n<header><h1>snippet_content</h1>\n\t      <ul id="navigation"><li><a href="http://google.com">Google</a></li>\n\t      <li><a href="http://amazon.com">Amazon</a></li>\n\t      \n\t      </ul></header>\n'

```


Transformations
----------------------

A transformation is a function that returns either a node or a collection of nodes.

Enlivepy defines several helper functions:


```python
	
	#Replaces the content of the element. There are two types of values: nodes or a collection of nodes.
	content("xyz", node_a, "abc")

	#Wraps selected node into the given tag
	wrap("div")
	#or
	wrap("div", {"class":"foo"})

	#Opposite to wrap, returns the content of the selected node
	unwrap

	#Sets given key value pairs as attributes of the selected node
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

The biggest difference lies in immutability. In the original __enlive__ when you do a transformation on a node, you just receive a copy of the said node. This is an advantage __Clojure__ possesses due to its persistent data structures. Of course, we can have a similar immutability model on Enlivepy. However, to achieve such a result, we need to do __deepcopy__ on every single transformation. As you might guess, proceeding in such a way would have a negative performance impact.

Other than that, there are a few missing pieces here:

- move transformations (to be added)
- beautiful dsl (Python doesn't have macros )
- ${vars} substitution (to be added)

