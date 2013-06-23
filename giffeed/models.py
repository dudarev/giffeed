from django.db import models
from picklefield.fields import PickledObjectField


class SearchKeyWord(models.Model):
    search_keyword = models.TextField(max_length=1000, unique=True)
    _gifs = PickledObjectField(db_column="gifs")
    updated_at = models.DateTimeField()

# http://www.korokithakis.net/posts/how-replace-django-model-field-property/
    @property
    def gifs(self):
        return self._gifs

    @gifs.setter
    def gifs(self, gifs):
        self._gifs = list(set(gifs))  # leave unique urls only

    def __unicode__(self):
        return self.search_keyword
