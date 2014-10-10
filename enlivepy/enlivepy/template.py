from .common import LxmlPathLoader, StringLoader, DecoratorArgMixin

class Template(object):

    #the path of the template
    template = None
    #loader is the loader for loading resources
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
