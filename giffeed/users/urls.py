from django.conf.urls import patterns, url
from giffeed.users.views import LoginView, LoginErrorView

urlpatterns = patterns(
    '',
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^login-error/$', LoginErrorView.as_view(), name='login-error'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'},
        name='logout')
)
