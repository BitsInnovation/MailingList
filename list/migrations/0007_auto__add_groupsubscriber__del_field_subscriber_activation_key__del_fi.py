# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GroupSubscriber'
        db.create_table(u'list_groupsubscriber', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['list.Group'])),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['list.Subscriber'])),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('activation_key', self.gf('django.db.models.fields.CharField')(default='', max_length=40, blank=True)),
        ))
        db.send_create_signal(u'list', ['GroupSubscriber'])

        # Deleting field 'Subscriber.activation_key'
        db.delete_column(u'list_subscriber', 'activation_key')

        # Deleting field 'Subscriber.confirmed'
        db.delete_column(u'list_subscriber', 'confirmed')

        # Removing M2M table for field group on 'Subscriber'
        db.delete_table(db.shorten_name(u'list_subscriber_group'))


    def backwards(self, orm):
        # Deleting model 'GroupSubscriber'
        db.delete_table(u'list_groupsubscriber')

        # Adding field 'Subscriber.activation_key'
        db.add_column(u'list_subscriber', 'activation_key',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=40),
                      keep_default=False)

        # Adding field 'Subscriber.confirmed'
        db.add_column(u'list_subscriber', 'confirmed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding M2M table for field group on 'Subscriber'
        m2m_table_name = db.shorten_name(u'list_subscriber_group')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscriber', models.ForeignKey(orm[u'list.subscriber'], null=False)),
            ('group', models.ForeignKey(orm[u'list.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscriber_id', 'group_id'])


    models = {
        u'list.email': {
            'Meta': {'object_name': 'Email'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'list.emailqueue': {
            'Meta': {'object_name': 'EmailQueue'},
            'email': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Email']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['list.Subscriber']"})
        },
        u'list.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'group': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['list.Group']", 'through': u"orm['list.GroupSubscriber']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['list']