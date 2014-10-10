"""
Tests for snippets and template structures
"""

from enlivepy.snippet import *
from enlivepy.template import *
from enlivepy.transformers import *


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

    header_snippet = HeaderSnippet(template=HEADER_SNIPPET)
    nodes = header_snippet(heading="custom_header",
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


#@snippet("header.html", "header")
#def transform_header(nodes, header_text=None):
#    pass


@snippet_from_str(HEADER_SNIPPET, "header")
def transform_header(nodes, heading="default", url_maps=None):

    at(nodes,
       "h1", content(heading))

    #now lets do the same thing for navigation
    at(nodes,
       "ul li", clone_for(url_maps,
                          "li", lambda url: set_attr(href=url["href"]),
                          "li", lambda url: content(url["content"])))

    return nodes



def test_snippet_fn():
    navigation = [
                   {"href":"/home/", "content":"Home"},
                   {"href":"/about/", "content":"About"},
                   {"href":"/projects/", "content":"Projects"}
    ]

    nodes = transform_header(heading="custom_header",
                             url_maps=navigation)

    #lets check some content
    h1_node = nodes[0].find("h1")
    assert h1_node.text == "custom_header"

    #check the navigation links
    ul_node = nodes[0].find("ul")
    assert len(ul_node) == len(navigation)

    for i, li in enumerate(ul_node):
        assert li.get("href") == navigation[i]["href"]
        assert li.text == navigation[i]["content"]


    #print emit(nodes)


BASE_HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <div class="content">
        Lorem opsum
    </div>
  </body>
</html>
"""



class SiteTemplate(StringTemplate):
    """
    Simple template
    """

    def transform(self, nodes, *args, **kwargs):
        """
        The transformation part is here
        :param nodes:
        :param args:
        :param kwargs:
        :return:
        """
        header = kwargs.get("header")
        if not header:
            raise Exception("missing header")

        cnt = kwargs.get("content")
        if not cnt:
            raise Exception("missing content")

        at(nodes,
           "body", prepend(header),
           "div.content", content(cnt))

        return nodes


@template_from_str(BASE_HTML_LAYOUT)
def base_template(node, header=None, cnt=None):

    at(node,
       "body", prepend(header),
       "div.content", content(cnt))

    return node



def test_site_template():
    navigation = [
                   {"href":"/home/", "content":"Home"},
                   {"href":"/about/", "content":"About"},
                   {"href":"/projects/", "content":"Projects"}
    ]

    header = transform_header(heading="custom_header",
                              url_maps=navigation)

    t = SiteTemplate(template=BASE_HTML_LAYOUT)
    template_node = t(header=header,
                      content="dynamic_content")

    #print(template_node)

    body_tag = template_node.find(".//body")
    header_tag = body_tag[0]
    div_tag = body_tag[1]

    assert header[0] == header_tag
    assert div_tag.tag == "div"
    assert div_tag.text == "dynamic_content"
    #print emit(template_node)


def test_site_template_from_dec():
    navigation = [
                   {"href":"/home/", "content":"Home"},
                   {"href":"/about/", "content":"About"},
                   {"href":"/projects/", "content":"Projects"}
    ]

    header = transform_header(heading="custom_header",
                              url_maps=navigation)

    template_node = base_template(header=header,
                                  cnt="dynamic_content")

    #print(template_node)
    body_tag = template_node.find(".//body")
    header_tag = body_tag[0]
    div_tag = body_tag[1]

    assert header[0] == header_tag
    assert div_tag.tag == "div"
    assert div_tag.text == "dynamic_content"
    #print emit(template_node)

