from lxml.html import builder as E
from lxml.html import fromstring

from enlivepy.transformers import *


HTML_STR = """
        <html>
            <table>
                <tr class="per_animal_row">
                    <td>
                        <input type="text" class="true_name" name="true_name"/>
                    </td>
                </tr>
            </table>
        </html>
        """

HTML_DIV = """
    <title>Some dummy title</title>
    <body>
        <div class="content">
            <b>Some bold text</b>
        </div>
    </body>
    """

def get_parse_node(s):
    return fromstring(s)



def test_at():
    node = get_parse_node(HTML_DIV)
    #lets add a new class has-error
    #and remove the bold tag
    at(node,
       "div.content", add_class("has-error"),
       "div.content b", None)

    #print emit(node)

    #now check for the consequences
    div_node = node.find(".//div")
    assert len(div_node) == 0
    assert div_node.get("class").strip() == "content has-error"



def test_content():
    node = get_parse_node(HTML_DIV)

    transform(node, "div b",
              content("hello_bold"))

    bold_tag = node.find(".//b")
    assert bold_tag.text.strip() == "hello_bold"


    #now try replace it with a span
    span_node = E.SPAN(E.CLASS("spanner_cls"), "span_content")
    transform(node, "div.content",
              content(span_node))

    div_tag = node.find(".//div")

    assert len(div_tag) == 1
    assert div_tag[0].text.strip() == "span_content"
    assert div_tag[0].tag == "span"

def test_append():

    node = get_parse_node(HTML_DIV)
    span_node = E.SPAN(E.CLASS("spanner_cls"), "span_add")

    at(node,
       "div.content", append(span_node),
       "div span", append("_later"))

    #print emit(node)
    div_tag = node.find(".//div")

    assert len(div_tag) == 2
    assert div_tag[1].text.strip() == "span_add_later"
    assert div_tag[1].tag == "span"



def test_clone_for():
    node = get_parse_node(HTML_STR)

    transform(node, "tr td",
              clone_for(range(0,3),
                        lambda i: content(str(i))))

    #now lets check and see
    tr_node = node.find(".//tr")
    assert len(tr_node) == 3

    for i, td in enumerate(tr_node):
        assert td.text.strip() == str(i)


def test_clone_for_lambda():
    node = get_parse_node(HTML_STR)

    #lets say now you want to duplicate the trs
    transform(node,
              "table tr",
              clone_for(range(1,4),
                        "tr > td", lambda i:content(str(i)),
                        "tr", lambda i: add_class("trclass_"+str(i)),
                        "tr", lambda i: remove_class("per_animal_row")))

    #you have done the transform lets emit it now
    #now check the contents of what was done
    table_node = node.find(".//table")
    #we should have 3 trs
    assert len(table_node) == 3

    for row, tr in enumerate(table_node):
        assert len(tr) == 1
        assert tr.tag == "tr"
        assert tr.get("class") == "trclass_{}".format(str(row+1))

        for td in tr:
            assert td.text.strip() == str(row+1)



def test_prepend():

    node = get_parse_node(HTML_DIV)
    #now try prepend some
    prepender = E.SPAN(E.CLASS("spanner_first"), "Some span data first")
    prepender2 = E.SPAN(E.CLASS("spanner_late"), "Some span data later")

    transform(node, "div.content", prepend(prepender, prepender2))

    div_node = node.find(".//div")

    assert len(div_node) == 3
    assert div_node[0].tag == "span"
    assert div_node[0].get("class") == "spanner_first"

    assert div_node[1].tag == "span"
    assert div_node[1].get("class") == "spanner_late"

    assert div_node[2].tag == "b"
    #print emit(node.find(".//div")[0])

    #preprend some text
    transform(node, "div.content", prepend("test1 ", "test2"))
    div_node = node.find(".//div")

    assert len(div_node) == 3
    assert div_node.text.strip() == "test1 test2"


def test_after():

    node = get_parse_node(HTML_DIV)
    after_node_first = E.DIV(E.CLASS("after_first"), "first div")
    after_node_second = E.DIV(E.CLASS("after_second"), "second div")

    transform(node, "div.content",
              after(after_node_first, after_node_second))

    #dprint emit(node)

    body_node = node.find(".//body")
    assert len(body_node) == 3
    assert body_node[1].tag == "div"
    assert body_node[1].get("class") == "after_first"

    assert body_node[2].tag == "div"
    assert body_node[2].get("class") == "after_second"

    #Lets put some text there
    transform(node, "div.content b",
              after("after_bold"))

    bold_node = node.find(".//div/b")
    assert bold_node.tail.strip() == "after_bold"


def test_before():

    node = get_parse_node(HTML_DIV)
    before_node_first = E.DIV(E.CLASS("before_first"), "first div")
    before_node_second = E.DIV(E.CLASS("before_second"), "second div")

    transform(node, "div.content",
              before(before_node_first, before_node_second))

    #dos some checks
    body_node = node.find(".//body")
    assert len(body_node) == 3
    assert body_node[0].tag == "div"
    assert body_node[0].get("class") == "before_first"

    assert body_node[1].tag == "div"
    assert body_node[1].get("class") == "before_second"

    assert body_node[2].tag == "div"
    assert body_node[2].get("class") == "content"


    #Lets put some text there
    transform(node, "div.content b",
              before("before_bold"))

    div_node = node.find(".//div[@class='content']")
    #print emit(div_node)
    assert div_node.text.strip() == "before_bold"


def test_substitute():
    node = get_parse_node(HTML_DIV)
    node_first = E.DIV(E.CLASS("first"), "first div")
    node_second = E.DIV(E.CLASS("second"), "second div")

    #substitute transformation
    transform(node, "div.content",
              substitute(node_first, node_second))

    #dos some checks
    body_node = node.find(".//body")
    assert len(body_node) == 2
    assert body_node[0].tag == "div"
    assert body_node[0].get("class") == "first"

    assert body_node[1].tag == "div"
    assert body_node[1].get("class") == "second"



def test_wrap_unwrap():
    node = get_parse_node(HTML_DIV)

    #now do the transformation
    transform(node,
              "div.content b",
              wrap("span", **{"class":"wrapper"}))


    div_node = node.find(".//div[@class='content']")
    assert len(div_node) == 1
    assert div_node[0].tag == "span"
    assert div_node[0].get("class") == "wrapper"

    #now unwrap it again
    transform(node,
              "div.content > span",
              unwrap)

    div_node = node.find(".//div[@class='content']")
    assert len(div_node) == 1
    assert div_node[0].tag == "b"


def test_set_remove_attr():
    node = get_parse_node(HTML_DIV)

    transform(node,
              "div.content",
              set_attr(**{"ng-app":"myapp"}))


    div_node = node.find(".//div[@class='content']")
    assert div_node.get("ng-app") == "myapp"

    #remove the same attr please
    transform(node,
              "div.content",
              remove_attr("ng-app"))

    assert div_node.get("ng-app") is None



def test_add_remove_class():

    node = get_parse_node(HTML_DIV)

    transform(node,
              "div.content",
              add_class("has_error"))

    #now check if it is there
    div_node = node.find(".//div")
    assert "has_error" in div_node.get("class").split()

    #now remove the class
    transform(node,
              "div.content",
              remove_class("has_error"))

    div_node = node.find(".//div")
    assert not "has_error" in div_node.get("class").split()
