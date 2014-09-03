"""
The reusable builder components of the library
With those you can create your templates and
reusable snippets !!!

TODO : Write more info here
"""

from lxml.html import fromstring, parse
from .template import select, transform

class StringLoader(object):

    def load(self, path):
        """
        Should return back a parsed node from the path
        :param path:
        :return:
        """
        return fromstring(path)



class LxmlPathLoader(object):

    def load(self, path):
        """
        Should return back a parsed node from the path
        :param path:
        :return:
        """
        return parse(path)


class Snippet(object):

    #the css selection string
    selection = None
    #the path of the template
    template = None
    #loader is the loader for loading resources
    loader_cls = None

    def __init__(self):

        self.loader = None
        if self.loader_cls:
            self.loader = self.loader_cls()

    def get_loader(self, *args, **kwargs):
        """
        Override the loader logic
        :return:
        """
        raise NotImplemented


    def get_selection(self, *args, **kwargs):
        """
        This should be implemented by those
        that inherit from this class
        :return:
        """
        raise NotImplemented


    def get_template(self, *args, **kwargs):
        raise NotImplemented



    def transform(self, nodes, *args, **kwargs):
        """
        This is where the real transformation is
        done. You should return back the node if needed
        :param node:
        :return:
        """
        raise NotImplemented



    def __call__(self, *args, **kwargs):
        """
        The real call of the snippet
        :param args:
        :param kwargs:
        :return:
        """
        sel = self.selection or self.get_selection(*args, **kwargs)
        loader = self.loader or self.get_loader(*args, **kwargs)
        template = self.template or self.get_template(*args, **kwargs)

        node = loader.load(template)
        nodes = select(node,sel)
        self.transform(nodes, *args, **kwargs)

        return nodes



class StringSnippet(Snippet):
    """
    Simple implementation for testing
    """
    loader_cls = StringLoader


    def get_template(self, *args, **kwargs):

        template_str = kwargs.get("template")
        if not template_str:
            raise Exception("template parameter missing")
        return template_str


    def get_selection(self, *args, **kwargs):

        sel = kwargs.get("sel")
        if not sel:
            raise Exception("Missing parameter sel")

        return sel


    def transform(self, nodes, *args, **kwargs):

        for n in nodes:
            for transform_fn in args:
                transform_fn(n)

        return nodes



def sniptest(template_str, selection, *transform_fns):
    """
    Simple fn wrapper to call the snippets
    :param template_str:
    :param selection:
    :param transform_fns:
    :return:
    """

    string_snip = StringSnippet()
    nodes = string_snip(*transform_fns, sel=selection, template=template_str)
    return nodes



