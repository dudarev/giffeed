from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin

from giffeed.views import search, search_form

admin.autodiscover()

from giffeed.core.views import HomePageView, UserPageView

urlpatterns = patterns(
    '',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^about$', TemplateView.as_view(template_name="about.html"),
        name='about'),
    url(r'^update$', 'giffeed.bots.views.update', name='update'),
    url(r'^(?P<username>[^/]+)$', UserPageView.as_view(), name='user'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'', include('social_auth.urls')),
    url(r'', include('giffeed.users.urls')),

    url(r'^search/form$', search_form, name='search-form'),
    url(r'^search/results$', search, name='search-results'),
    (r'^search/result',
    TemplateView.as_view(template_name="search_results.html")),
)
