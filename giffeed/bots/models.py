from django.db import models


class Bot(models.Model):
    name = models.SlugField()
    url = models.URLField()
