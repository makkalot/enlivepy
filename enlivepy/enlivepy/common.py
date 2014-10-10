from lxml.html import fromstring, parse

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


class DecoratorArgMixin(object):
    """
    Useful for passing the transformer from outside
    """
    def transform(self, nodes, *args, **kwargs):

        transform_fn = self.init_kwargs.get("transform_fn")
        if not transform_fn:
            raise Exception("transform_fn missing")

        return transform_fn(nodes, *args, **kwargs)
