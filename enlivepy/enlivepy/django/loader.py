import os

from lxml.html import fromstring

from django.template.base import TemplateDoesNotExist
from django.template.loader import BaseLoader
from django.template.loaders.app_directories import app_template_dirs
from django.conf import settings

from enlivepy.template import Template
from enlivepy.snippet import Snippet
from enlivepy.transformers import emit
from enlivepy.django.registry import registry

#This loader is different from that below
#this is for loading the .html files from system
class DjangoDirPathLoader(object):


    def load(self, path):
        """
        Should return back a parsed node from the path
        :param path:
        :return:
        """
        app_dirs = list(app_template_dirs) + list(settings.TEMPLATE_DIRS)
        #print "APPDIRS : ",app_dirs

        for d in app_dirs:
            fpath = os.path.join(d, path)
            #print "CHECK : ",fpath
            if os.path.exists(fpath):
                str_body = open(fpath).read()
                return fromstring(str_body)

        raise TemplateDoesNotExist("The resource file : %s not found"%path)

class DjangoTemplate(Template):

    loader_cls = DjangoDirPathLoader

    def render(self, context):
        # flatten the Django Context into a single dictionary.
        context_dict = {}

        for d in context.dicts:
            #print "KEYS : ", d.keys()
            context_dict.update(d)

        #call the transformer part
        node = self.__call__(**context_dict)
        #emit the string representation
        return emit(node)


class DjangoSnippet(Snippet):

    loader_cls = DjangoDirPathLoader



class EnlivepyLoader(BaseLoader):
    is_usable = True
    env = registry

    def load_template(self, template_name, template_dirs=None):
        try:
            #print "REGISTERED  : ",self.env.registered
            template = self.env.registered[template_name]
        except KeyError:
            raise TemplateDoesNotExist(template_name)
        return template, template_name

