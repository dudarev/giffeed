from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from giffeed.core.views import HomePageView, UserPageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^(?P<username>[^/]+)$', UserPageView.as_view(), name='user'),
    url(r'^admin/', include(admin.site.urls)),
)

