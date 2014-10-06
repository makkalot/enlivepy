from django.core.urlresolvers import reverse, reverse_lazy
from django.forms.models import ModelForm
from django.http.response import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render

from django.views.generic.base import TemplateView, View
from enlivetest.models import TodoItem
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import UpdateView, DeleteView


class HomePageView(TemplateView):

    template_name = "site_tmpl"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['cool_context'] = "cooler"
        context["header"] = "EnlivePy Header"
        context["content"] = "Dynamic Header"

        return context


class TodoIndexView(TemplateView):

    template_name = "todo_index"



class TodoItemForm(ModelForm):
    class Meta:
        model = TodoItem


class TodoListView(TemplateView):

    template_name = "todo_list"
    form_cls = TodoItemForm

    def get_context_data(self, **kwargs):
        """
        Add some todo items  here
        :param kwargs:
        :return:
        """
        todos = TodoItem.objects.all()
        completed = todos.filter(done=True)

        #print kwargs

        if kwargs.has_key("done"):
            done = kwargs.get("done")
            if done == "completed":
                todos = todos.filter(done=True)
            else:
                todos = todos.filter(done=False)


        context = super(TodoListView, self).get_context_data(**kwargs)

        context["todos"] = todos
        context['completed'] = completed.count()
        context['todo_form'] = TodoItemForm()
        return context


    def post(self, request, *args, **kwargs):
        form = self.form_cls(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("todo_index"))

        return HttpResponseBadRequest("Invalid Data")


class TodoToggleUpdateView(SingleObjectMixin, View):

    model = TodoItem

    def post(self, request, *args, **kwargs):
        """
        Updates or toggles the item
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #print request.POST
        self.object = self.get_object()
        if request.POST["done"] == "true":
            self.object.done = False
        else:
            self.object.done = True

        self.object.save()

        return HttpResponseRedirect(reverse("todo_index"))


class TodoDeleteView(DeleteView):
    success_url = reverse_lazy("todo_index")
    model = TodoItem


class TodoDeleteBulkView(View):
    """
    Deletes all of the completed todo lists
    """
    def post(self, request, *args, **kwargs):
        """
        Updates or toggles the item
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #print request.POST
        TodoItem.objects.filter(done=True).delete()
        return HttpResponseRedirect(reverse("todo_index"))



