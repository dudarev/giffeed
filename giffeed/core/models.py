from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    tag = models.TextField()

    def __unicode__(self):
        return self.tag


class Post(models.Model):
    user = models.ForeignKey(User)
    gif_url = models.URLField(null=True, unique=True)
    time_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)
    comment = models.TextField()
