from django.conf import settings
from django.shortcuts import HttpResponse, render_to_response, RequestContext, redirect
from django.http import HttpResponseBadRequest

import transmissionrpc
from json import dumps
import tempfile
from base64 import b64encode
from os import unlink

from django.views.decorators.csrf import csrf_exempt

from transmission.models import Torrent, Group

def api_add_torrent(request):
    if request.method == 'POST':
        with tempfile.NamedTemporaryFile('w+b', delete=False) as fp:
            f = request.FILES.get('torrent')
            tf = fp.name
            for chunk in f.chunks():
                fp.write(chunk)

        tc = transmissionrpc.Client(
            settings.TRANSMISSION['default']['HOST'],
            port=settings.TRANSMISSION['default']['PORT'],
            user=settings.TRANSMISSION['default']['USER'],
            password=settings.TRANSMISSION['default']['PASSWORD'])

        fp.close()
        fp = open(tf, 'r')
        tc.add_torrent(b64encode(fp.read()))
        fp.close()
        unlink(tf)

        return redirect('/')
    else:
        return HttpResponseBadRequest(
            content=dumps({
                'status': 'error',
                'reason': 'Request method should be POST'
            }), content_type='application/json'
        )

def api_action(request, id, action):
    if request.method == 'POST':
        tc = transmissionrpc.Client(
            settings.TRANSMISSION['default']['HOST'],
            port=settings.TRANSMISSION['default']['PORT'],
            user=settings.TRANSMISSION['default']['USER'],
            password=settings.TRANSMISSION['default']['PASSWORD'])
    else:
        return HttpResponseBadRequest(
            content=dumps({
                'status': 'error',
                'reason': 'Request method should be POST'
            }), content_type='application/json'
        )


    torrent = tc.get_torrent(torrent_id=id)

    if action == 'delete':
        tc.remove_torrent(torrent.id)
    elif action == 'start':
        tc.start_torrent(torrent.id)
    elif action == 'stop':
        tc.stop_torrent(torrent.id)
    else:
        return HttpResponseBadRequest(
            content=dumps({
                'status': 'error',
                'reason': 'No such method %s' % action
            }), content_type='application/json'
        )

def api_list(request):
    tc = transmissionrpc.Client(
        settings.TRANSMISSION['default']['HOST'],
        port=settings.TRANSMISSION['default']['PORT'],
        user=settings.TRANSMISSION['default']['USER'],
        password=settings.TRANSMISSION['default']['PASSWORD'])

    return HttpResponse(
        content=dumps([{
            'id': x.id,
            'name': x.name,
            'status': x.status,
            'progress': x.progress
        } for x in tc.get_torrents()]),
        content_type='application/json'
    )


def index(request):
    return render_to_response(
        'transmission/list.html',
        {'nav': 'transmission'},
        context_instance=RequestContext(request))
