#!/usr/bin/env python

import logging
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blackbox.settings")

from django.conf import settings

import transmissionrpc
from transmission.models import Torrent

if __name__ == "__main__":
    tc = transmissionrpc.Client(
        settings.TRANSMISSION['default']['HOST'],
        port=settings.TRANSMISSION['default']['PORT'],
        user=settings.TRANSMISSION['default']['USER'],
        password=settings.TRANSMISSION['default']['PASSWORD'])

    rpclist = tc.get_torrents()
    data = {}
    for t in rpclist:
        torrent, created = Torrent.objects.get_or_create(
            hash=t.hashString
        )

        if torrent.status != t.status or torrent.progress not in [
            t.progress, t.recheckProgress]:
            torrent.status = t.status
            torrent.progress = t.progress or t.recheckProgress

            torrent.save()

        if created:
            torrent.name = t.name
            torrent.save()

        data[t.hashString] = {
            'hash': t.hashString,
            }

    for t in Torrent.objects.all():
        try:
            data[t.hash]['name'] = t.name
        except KeyError:
            t.delete()
            del(data[t.hash])
