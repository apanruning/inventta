# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Idea'
        db.create_table('inventta_idea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(db_index=True, max_length=50, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=126, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('rendered', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.SlugField')(default='anon', max_length=20, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('metadata', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
        ))
        db.send_create_signal('inventta', ['Idea'])


    def backwards(self, orm):
        
        # Deleting model 'Idea'
        db.delete_table('inventta_idea')


    models = {
        'inventta.idea': {
            'Meta': {'object_name': 'Idea'},
            'author': ('django.db.models.fields.SlugField', [], {'default': "'anon'", 'max_length': '20', 'db_index': 'True'}),
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'rendered': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '126', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['inventta']
