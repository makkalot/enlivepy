from enlivepy.django.loader import DjangoTemplate
from enlivepy.django.registry import register
from enlivepy.template import prepend, content, at

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



#register the template
register("site_tmpl", ContentTemplate())