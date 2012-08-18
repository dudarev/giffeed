import datetime
import re, urllib2

from django.db import models


class Bot(models.Model):
    name = models.SlugField()
    url = models.URLField()
    # time in past for new bots
    last_run_at = models.DateTimeField(default=datetime.datetime(2000,1,1))
    source = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.name

    def parse_url(self, file_name=None):

        if file_name:
            feed = open(file_name, 'r').read()
        else:
            url_request = urllib2.Request(self.url)
            response = urllib2.urlopen(url_request)
            feed = response.read()

        gif_regex = re.compile('http[^\'" \n>]+.gif', re.IGNORECASE)
        links = set(re.findall(gif_regex, feed))

        # special cases

        # ignore links with topsy from topsy
        if self.source == 'topsy':
            links = [l for l in links if not 'topsy' in l]
        else:
            links = list(links)

        return links

