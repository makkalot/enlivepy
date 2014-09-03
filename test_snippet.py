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

        at(nodes,
           "h1", content(heading))

        #now lets do the same thing for navigation
        

        return nodes


def test_header_snippet():

    header_snippet = HeaderSnippet()
    nodes = header_snippet(template=HEADER_SNIPPET,
                           heading="custom_header")

    print emit(nodes)