import datetime
import re, urllib2

from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.db import IntegrityError, connection


class Bot(models.Model):

    user = models.OneToOneField(User, null=True, blank=True)
    #  when creating bot accounts in admin panel start them with '-'
    name = models.SlugField(verbose_name="Bot name (start with '-')")
    url = models.URLField()
    # time in past for new bots
    last_run_at = models.DateTimeField(default=datetime.datetime(2000,1,1))
    source = models.CharField(max_length=30, null=True, blank=True)
    
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


@receiver(post_save, sender=Bot)
def bot_save_handler(sender, instance, created, **kwargs):
    if created:
        try:
            u = User.objects.create_user(instance.name, 'dudarev@gmail.com', '')
            u.save()
        except IntegrityError:
            connection._rollback()
            return
        instance.user = u
        instance.save()
