class AlreadyRegistered(Exception):
    pass

class NotRegistered(Exception):
    pass

class TemplateRegistry(object):
    """
    A dictionary that contains permission instances and their labels.
    """
    _registry = {}

    def register(self, name, template_or_fn):
        if name in self._registry:
            raise AlreadyRegistered(
                'The template %s is already registered' % name)

        self._registry[name] = template_or_fn

    def unregister(self, name):
        if name not in self._registry:
            raise NotRegistered('The model %s is not registered' % name)
        del self._registry[name]

    def _get_registered(self):
        return self._registry
    registered = property(_get_registered)


registry = TemplateRegistry()
register = registry.register
unregister = registry.unregister
registered = registry.registered