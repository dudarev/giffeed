import datetime
import re, urllib2

from django.db import models


class Bot(models.Model):
    name = models.SlugField()
    url = models.URLField()
    # time in past for new bots
    last_run_at = models.DateTimeField(default=datetime.datetime(2000,1,1))

    def __unicode__(self):
        return self.name

    def parse_url(self):
        url_request = urllib2.Request(self.url)
        response = urllib2.urlopen(url_request)
        feed = response.read()
        gif_regex = re.compile('http[^\'" >]+.gif', re.IGNORECASE)
        return re.findall(gif_regex, feed)
