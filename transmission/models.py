import datetime
from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name


class Torrent(models.Model):
    hash = models.CharField(max_length=40)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(
        Group, related_name='torrents',
        null=True, blank=True)
    status = models.CharField(max_length=32, default=None, null=True)
    progress = models.IntegerField(
        max_length=3, default=0,
        null=True, blank=True)
    created = models.DateTimeField(
        default=datetime.datetime.now(),
        auto_now_add=True)

    def __unicode__(self):
        return self.name


class File(models.Model):
    filename = models.CharField(max_length=255)
    torrent = models.ForeignKey(Torrent, related_name='files')
    created = models.DateTimeField(
        default=datetime.datetime.now(),
        auto_now_add=True)

    def __unicode__(self):
        return self.filename


class Hardlink(models.Model):
    token = models.CharField(max_length=64, db_index=True)
    file = models.ForeignKey(File, related_name='hardlinks')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='users')

    def __unicode__(self):
        return self.token


class View(models.Model):
    file = models.ForeignKey(File, related_name='views')
    user = models.ForeignKey(User, related_name='viewed')
