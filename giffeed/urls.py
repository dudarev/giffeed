from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from giffeed.core.views import HomePageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

