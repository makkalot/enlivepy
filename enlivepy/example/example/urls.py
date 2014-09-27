from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings

from django.conf.urls.static import static

from enlivetest.views import HomePageView
from enlivetest.views import TodoIndexView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^index/', TodoIndexView.as_view(), name="todo_index"),

    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

