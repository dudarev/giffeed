from django.conf.urls import patterns, url
from giffeed.upload.views import upload


urlpatterns = patterns(
    '',
    (url(r'^upload/form$', upload, name='upload'))
)
