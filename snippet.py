"""
The reusable builder components of the library
With those you can create your templates and
reusable snippets !!!

TODO : Write more info here
"""
from functools import wraps

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

    def __init__(self, *args, **kwargs):
        self.init_args = args
        self.init_kwargs = kwargs

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

        sel = self.init_kwargs.get("sel")
        if not sel:
            raise Exception("Missing parameter sel")

        return sel


    def get_template(self, *args, **kwargs):

        template_str = self.init_kwargs.get("template")
        if not template_str:
            raise Exception("template parameter missing")
        return template_str



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



    def transform(self, nodes, *args, **kwargs):

        for n in nodes:
            for transform_fn in args:
                transform_fn(n)

        return nodes



class DecoratorArgMixin(object):

    """
    Useful for passing the transformer from outside
    """
    def transform(self, nodes, *args, **kwargs):

        transform_fn = self.init_kwargs.get("transform_fn")
        if not transform_fn:
            raise Exception("transform_fn missing")

        return transform_fn(nodes, *args, **kwargs)


class DecoratedSnippet(DecoratorArgMixin, Snippet):
    pass


class DecoratedStringSnippet(DecoratorArgMixin, StringSnippet):
    pass


def sniptest(template_str, selection, *transform_fns):
    """
    Simple fn wrapper to call the snippets
    :param template_str:
    :param selection:
    :param transform_fns:
    :return:
    """

    string_snip = StringSnippet(template=template_str,
                                sel=selection)
    nodes = string_snip(*transform_fns)
    return nodes



#we should be able to define the snippets via decorators too
def snippet(path, selection):

    #that way we cache them for further usage !!!
    def _wrapper(f):
        decorator_snippet = DecoratedSnippet(transform_fn=f,
                                             template=path,
                                             sel=selection)

        return decorator_snippet

    return _wrapper

def snippet_from_str(snip_str, selection):

    #that way we cache them for further usage !!!
    def _wrapper(f):
        decorator_snippet = DecoratedStringSnippet(transform_fn=f,
                                                   template=snip_str,
                                                   sel=selection)

        return decorator_snippet

    return _wrapper


class Template(object):

    #the path of the template
    template = None
    #loader is the loader for loading resourcess
    loader_cls = LxmlPathLoader

    def __init__(self, *args, **kwargs):

        self.init_args = args
        self.init_kwargs = kwargs

        self.loader = None
        if self.loader_cls:
            self.loader = self.loader_cls()


    def get_loader(self, *args, **kwargs):
        """
        Override the loader logic
        :return:
        """
        raise NotImplemented()



    def get_template(self, *args, **kwargs):
        """
        The default implementation for get_template
        You can override it too if needed
        :param args:
        :param kwargs:
        :return:
        """
        if not self.init_kwargs.has_key("template"):
            raise Exception("No template parameter is supplied")

        return self.init_kwargs.get("template")


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
        loader = self.loader or self.get_loader(*args, **kwargs)
        template = self.template or self.get_template(*args, **kwargs)

        node = loader.load(template)
        self.transform(node, *args, **kwargs)

        return node



class StringTemplate(Template):

    loader_cls = StringLoader


class DecoratedTemplate(DecoratorArgMixin, Template):
    pass

class DecoratedStringTemplate(DecoratorArgMixin, StringTemplate):
    pass


def template(path):

    #that way we cache them for further usage !!!
    def _wrapper(f):
        decorator_template = DecoratedTemplate(transform_fn=f,
                                                template=path)

        return decorator_template

    return _wrapper


def template_from_str(path):

    #that way we cache them for further usage !!!
    def _wrapper(f):
        decorator_template = DecoratedStringTemplate(transform_fn=f,
                                                     template=path)

        return decorator_template

    return _wrapper
