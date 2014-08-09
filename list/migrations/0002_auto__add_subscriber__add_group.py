# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subscriber'
        db.create_table(u'list_subscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal(u'list', ['Subscriber'])

        # Adding model 'Group'
        db.create_table(u'list_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'list', ['Group'])

        # Adding M2M table for field subscribers on 'Group'
        m2m_table_name = db.shorten_name(u'list_group_subscribers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'list.group'], null=False)),
            ('subscriber', models.ForeignKey(orm[u'list.subscriber'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'subscriber_id'])


    def backwards(self, orm):
        # Deleting model 'Subscriber'
        db.delete_table(u'list_subscriber')

        # Deleting model 'Group'
        db.delete_table(u'list_group')

        # Removing M2M table for field subscribers on 'Group'
        db.delete_table(db.shorten_name(u'list_group_subscribers'))


    models = {
        u'list.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'subscribers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['list.Subscriber']", 'symmetrical': 'False'})
        },
        u'list.subscriber': {
            'Meta': {'object_name': 'Subscriber'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['list']