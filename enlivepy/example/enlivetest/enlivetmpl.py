from functools import partial
import os

from enlivepy.django.loader import DjangoTemplate, DjangoSnippet
from enlivepy.django.registry import register
from enlivepy.template import prepend, content, at, transform, set_attr, clone_for, select, snip_at


class ContentTemplate(DjangoTemplate):

    template = "base.html"

    def transform(self, nodes, *args, **kwargs):
        """
        The transformation part is here
        :param nodes:
        :param args:
        :param kwargs:
        :return:
        """
        #print "KWARGS : ",kwargs

        header = kwargs.get("header")
        if not header:
            raise Exception("missing header")

        cnt = kwargs.get("content")
        if not cnt:
            raise Exception("missing content")

        #print "NODES : ",nodes

        dyn_cnt = "{} - {}".format(cnt, str(kwargs["user"]))

        at(nodes,
           "head > title", content(header),
           "div.content", content(dyn_cnt))

        return nodes


class BaseMediaUrlTemplate(DjangoTemplate):

    def transform(self, nodes, *args, **kwargs):

        if not kwargs.get("STATIC_URL"):
            raise Exception("STATIC_URL not set")

        media_url = kwargs.get("STATIC_URL")
        #print "MEDIA : ",media_url

        #the next step is to run the at command
        at(nodes,
           "script", partial(self.trans_path, media_url, "script", "src"),
           "link",   partial(self.trans_path, media_url, "link", "href"))


    def trans_path(self, media_url, tag_name, attr_name, node):

        path = node.get(attr_name)
        if not path:
            return

        path = path.strip()
        if path.startswith("http") or not path:
            #do nothing in this case
            return

        fpath = ""
        if path.startswith(media_url[1:]):
            fpath = "".join(["/", path])
        else:
            fpath = os.path.join(media_url, path)

        attr_fn = set_attr(**{attr_name:fpath})
        return transform(node, tag_name, attr_fn)


class TodoNavSnippet(DjangoSnippet):

    template = "logonav/nav.html"
    selection = "nav.navbar"

    menu_items = ("Home", "About", "Services", "Contact")

    def transform(self, nodes, *args, **kwargs):
        navs_fn = clone_for(self.menu_items,
                            "li > a", lambda i: content(i),
                            "li > a", lambda i: set_attr(href="/"+i.lower()+"/"))
        at(nodes, "ul.nav > li", navs_fn)
        return nodes




class TodoIndex(BaseMediaUrlTemplate):

    template = "logonav/index.html"

    def transform(self, nodes, *args, **kwargs):
        #call the previous one first
        super(TodoIndex, self).transform(nodes, *args, **kwargs)
        #prepend the navigation snippet
        nav_snip = TodoNavSnippet()
        navbar = nav_snip(*args, **kwargs)

        #lets do some operation
        #insert the navigation here
        hnode = snip_at(nodes, "div.col-lg-12 > h1",
                        "div.col-lg-12 > h1", content("Index Todo List"))

        at(nodes,
           "body", prepend(navbar),
           "div.col-lg-12", content(hnode))


#register the template
register("site_tmpl", ContentTemplate())
register("todo_index", TodoIndex())
