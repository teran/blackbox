# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'File.created'
        db.add_column(u'transmission_file', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 2, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'Torrent.status'
        db.add_column(u'transmission_torrent', 'status',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=32, null=True),
                      keep_default=False)

        # Adding field 'Torrent.progress'
        db.add_column(u'transmission_torrent', 'progress',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Torrent.created'
        db.add_column(u'transmission_torrent', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 5, 2, 0, 0), auto_now_add=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'File.created'
        db.delete_column(u'transmission_file', 'created')

        # Deleting field 'Torrent.status'
        db.delete_column(u'transmission_torrent', 'status')

        # Deleting field 'Torrent.progress'
        db.delete_column(u'transmission_torrent', 'progress')

        # Deleting field 'Torrent.created'
        db.delete_column(u'transmission_torrent', 'created')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'transmission.file': {
            'Meta': {'object_name': 'File'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'torrent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'files'", 'to': u"orm['transmission.Torrent']"})
        },
        u'transmission.group': {
            'Meta': {'object_name': 'Group'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'transmission.hardlink': {
            'Meta': {'object_name': 'Hardlink'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'hardlinks'", 'to': u"orm['transmission.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'users'", 'to': u"orm['auth.User']"})
        },
        u'transmission.torrent': {
            'Meta': {'object_name': 'Torrent'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 2, 0, 0)', 'auto_now_add': 'True', 'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'torrents'", 'null': 'True', 'to': u"orm['transmission.Group']"}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'progress': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '32', 'null': 'True'})
        },
        u'transmission.view': {
            'Meta': {'object_name': 'View'},
            'file': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'views'", 'to': u"orm['transmission.File']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewed'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['transmission']