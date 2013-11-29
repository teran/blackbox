from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(max_length=7)

    def __unicode__(self):
        return self.name


class Torrent(models.Model):
    hash = models.CharField(max_length=32)
    name = models.CharField(max_length=255)
    group = models.ForeignKey(Group, related_name='torrents',
                              null=True, blank=True)

    def __unicode__(self):
        return self.name


class File(models.Model):
    filename = models.CharField(max_length=255)
    torrent = models.ForeignKey(Torrent, related_name='files')

    def __unicode__(self):
        return self.filename


class Hardlink(models.Model):
    token = models.CharField(max_length=64)
    file = models.ForeignKey(File, related_name='hardlinks')
    created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.token
