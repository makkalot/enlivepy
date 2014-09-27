from django.conf.urls import patterns, include, url
from django.contrib import admin

from enlivetest.views import HomePageView


urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
