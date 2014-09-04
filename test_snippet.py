"""
Tests for snippets and template structures
"""

from .snippet import sniptest, StringSnippet
from .template import *

HTML_DIV = """
    <title>Some dummy title</title>
    <body>
        <div class="content">
            <b>Some bold text</b>
        </div>
    </body>
    """

HEADER_SNIPPET = """
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
"""

def test_sniptest():

    nodes = sniptest(HTML_DIV,
                "div.content",
                content("hello_content"),
                add_class("has_warning"))

    assert len(nodes) == 1

    div_node = nodes[0]
    print emit(div_node)
    assert div_node.tag == "div"
    assert div_node.text == "hello_content"
    assert "has_warning" in div_node.get("class").split()



class HeaderSnippet(StringSnippet):

    selection = "header"

    def transform(self, nodes, *args, **kwargs):

        heading = kwargs.get("heading")
        if not heading:
            raise Exception("heading param missing")

        url_maps = kwargs.get("navigation")
        if not url_maps:
            raise Exception("navigation is missing")



        at(nodes,
           "h1", content(heading))

        #now lets do the same thing for navigation
        at(nodes,
           "ul li", clone_for(url_maps,
                              "li", lambda url: set_attr(href=url["href"]),
                              "li", lambda url: content(url["content"])))

        return nodes


def test_header_snippet():

    navigation = [
                   {"href":"/home/", "content":"Home"},
                   {"href":"/about/", "content":"About"},
                   {"href":"/projects/", "content":"Projects"}
    ]

    header_snippet = HeaderSnippet()
    nodes = header_snippet(template=HEADER_SNIPPET,
                           heading="custom_header",
                           navigation=navigation)

    #lets check some content
    h1_node = nodes[0].find("h1")
    assert h1_node.text == "custom_header"

    #check the navigation links
    ul_node = nodes[0].find("ul")
    assert len(ul_node) == len(navigation)

    for i, li in enumerate(ul_node):
        assert li.get("href") == navigation[i]["href"]
        assert li.text == navigation[i]["content"]
