# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bot.source'
        db.add_column('bots_bot', 'source',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bot.source'
        db.delete_column('bots_bot', 'source')


    models = {
        'bots.bot': {
            'Meta': {'object_name': 'Bot'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2000, 1, 1, 0, 0)'}),
            'name': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['bots']