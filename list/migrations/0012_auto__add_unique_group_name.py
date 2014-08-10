# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Group', fields ['name']
        db.create_unique(u'list_group', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Group', fields ['name']
        db.delete_unique(u'list_group', ['name'])


    models = {
        u'list.email': {
            'Meta': {'object_name': 'Email'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'list.emailqueue': {
            'Meta': {'object_name': 'EmailQueue'},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Email']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'send_date': ('django.db.models.fields.DateField', [], {}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Subscriber']"})
        },
        u'list.group': {
            'Meta': {'object_name': 'Group'},
            'from_email': ('django.db.models.fields.EmailField', [], {'default': "'me@chrisbartos.com'", 'max_length': '75'}),
            'from_name': ('django.db.models.fields.CharField', [], {'default': "'Chris Bartos'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'list.groupsubscriber': {
            'Meta': {'object_name': 'GroupSubscriber'},
            'activation_key': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40', 'blank': 'True'}),
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Subscriber']"})
        },
        u'list.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['list.Group']", 'through': u"orm['list.GroupSubscriber']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscribe_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['list']