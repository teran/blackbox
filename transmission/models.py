from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

class Torrent(models.Model):
    tid = models.IntegerField()
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, related_name='torrents', null=True, blank=True)
