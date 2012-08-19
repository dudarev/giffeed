from django.db import models
from django.contrib.auth.models import User

class GIF(models.Model):
    url = models.URLField()

class Post(models.Model):
    user = models.ForeignKey(User)
    gif = models.ForeignKey(GIF)
