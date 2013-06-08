from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from .views import LoginView, LoginErrorView

from django.contrib import admin
admin.autodiscover()

from giffeed.core.views import HomePageView, UserPageView

urlpatterns = patterns('',
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^about$', TemplateView.as_view(template_name="about.html"), name='about'),
    url(r'^update$', 'giffeed.bots.views.update', name='update'),
    url(r'^(?P<username>[^/]+)$', UserPageView.as_view(), name='user'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login-error/$', LoginErrorView.as_view(), name='login-error'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout')
)

