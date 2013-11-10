from django.conf import settings
from django.shortcuts import HttpResponse, render_to_response, RequestContext

import transmissionrpc
from json import dumps

from transmission.models import Torrent, Group

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
        } for x in tc.get_torrents()])
    )


def index(request):
    return render_to_response(
        'transmission/list.html',
        {},
        context_instance=RequestContext(request))
