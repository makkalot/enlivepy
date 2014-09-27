from django.shortcuts import render

from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    template_name = "site_tmpl"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['cool_context'] = "cooler"
        context["header"] = "EnlivePy Header"
        context["content"] = "Dynamic Header"

        return context
