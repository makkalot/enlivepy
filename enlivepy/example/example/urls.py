from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static

from enlivetest.views import HomePageView
from enlivetest.views import TodoIndexView
from enlivetest.views import TodoListView, TodoDeleteView, TodoToggleUpdateView, TodoDeleteBulkView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^index/', TodoIndexView.as_view(), name="todo_index"),
    url(r'^list/(?P<done>\w+)/', TodoListView.as_view(), name="todo_index_filter"),
    url(r'^list/', TodoListView.as_view(), name="todo_index"),
    url(r'^todo/delele/completed/$', TodoDeleteBulkView.as_view(), name="todo_delete_completed"),
    url(r'^todo/delele/(?P<pk>[0-9]+)/$', TodoDeleteView.as_view(), name="todo_delete"),
    url(r'^todo/update/(?P<pk>[0-9]+)/$', TodoToggleUpdateView.as_view(), name="todo_update"),


    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

