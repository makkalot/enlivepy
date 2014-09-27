__author__ = 'makkalot'

import sys


LOADING = False

def autodiscover():
    """
    Goes and imports the permissions submodule of every app in INSTALLED_APPS
    to make sure the templates classes/fns are registered correctly.
    """
    global LOADING
    if LOADING:
        return
    LOADING = True

    import imp
    from django.conf import settings

    for app in settings.INSTALLED_APPS:
        try:
            __import__(app)
            app_path = sys.modules[app].__path__
        except AttributeError:
            continue
        try:
            imp.find_module('enlivetmpl', app_path)
        except ImportError:
            continue
        __import__("%s.enlivetmpl" % app)
        app_path = sys.modules["%s.enlivetmpl" % app]

    LOADING = False