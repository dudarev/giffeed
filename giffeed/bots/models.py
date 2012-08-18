import datetime

from django.db import models


class Bot(models.Model):
    name = models.SlugField()
    url = models.URLField()
    # time in past for new bots
    last_run_at = models.DateTimeField(default=datetime.datetime(2000,1,1))

    def __unicode__(self):
        return self.name
