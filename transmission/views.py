import transmissionrpc
import tempfile
import mimetypes
from base64 import b64encode
from json import dumps
from os import unlink, path
from hashlib import sha1
from random import random
from datetime import datetime, timedelta
from urllib import quote

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import HttpResponse, render_to_response, \
    RequestContext, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from transmission.models import Torrent, Group, File, Hardlink, View


@csrf_exempt
@login_required
def api_action(request, hash, action):
    """
    Common method to do some of actions like:

     * delete torrent
     * start downloading/seeding
     * stop downloading/seeding
     * get info
     * update torrent name
    """
    tc = transmissionrpc.Client(
        settings.TRANSMISSION['default']['HOST'],
        port=settings.TRANSMISSION['default']['PORT'],
        user=settings.TRANSMISSION['default']['USER'],
        password=settings.TRANSMISSION['default']['PASSWORD'])

    torrent = tc.get_torrent(hash)
    torrent.name = Torrent.objects.get(hash=hash).name

    if action == 'delete':
        tc.remove_torrent(hash, delete_data=True)
    elif action == 'start':
        tc.start_torrent(hash)
    elif action == 'stop':
        tc.stop_torrent(hash)
    elif action == 'info':
        if request.method == 'GET':
            files = torrent.files()
            data = []
            for f in files:
                tobj = Torrent.objects.get(hash=hash)
                file, created = File.objects.get_or_create(
                    torrent=tobj,
                    filename=files[f]['name']
                )
                if settings.EMBEDED_PLAYER:
                    data.append({
                        'filename': '%s' % path.basename(files[f]['name']),
                        'link': path.join(settings.FILE_URL, str(file.pk)),
                        'viewed': View.objects.filter(
                            file=file, user=request.user).count()
                    })
                else:
                    data.append({
                        'filename': '%s' % path.basename(files[f]['name']),
                        'link': path.join(settings.HARDLINK_URL, str(file.pk)) +
                                '?redirect=1' % file.pk,
                        'viewed': View.objects.filter(
                            file=file, user=request.user).count()
                    })

            return HttpResponse(
                content=dumps({
                    'hash': hash,
                    'name': torrent.name,
                    'status': torrent.status,
                    'progress': torrent.progress,
                    'magnetLink': torrent.magnetLink,
                    'files': sorted(data)
                })
            )
        elif request.method == 'POST':
            t = Torrent.objects.get(hash=hash)
            t.name = request.POST.get('name', torrent.name)
            t.save()
            return HttpResponse(
                content=dumps({
                    'status': 'ok'
                }), content_type='application/json'
            )
        else:
            return HttpResponseBadRequest(
                content=dumps({
                    'status': 'error',
                    'reason': 'request type should be GET or POST'
                }), content_type='application/json'
            )
    elif action == 'verify':
        tc.verify_torrent(hash)
    else:
        return HttpResponseBadRequest(
            content=dumps({
                'status': 'error',
                'reason': 'No such method %s' % action
            }), content_type='application/json'
        )
    return HttpResponse(
        content=dumps({
            'status': 'ok'
        }), content_type='application/json'
    )

@login_required
def api_add_torrent(request):
    """
    Add torrent with a torrent file, http link or magnet link
    """
    if request.method == 'POST':
        tc = transmissionrpc.Client(
            settings.TRANSMISSION['default']['HOST'],
            port=settings.TRANSMISSION['default']['PORT'],
            user=settings.TRANSMISSION['default']['USER'],
            password=settings.TRANSMISSION['default']['PASSWORD'])

        if 'torrent' in request.FILES:
            with tempfile.NamedTemporaryFile('w+b', delete=False) as fp:
                f = request.FILES.get('torrent')
                tf = fp.name
                for chunk in f.chunks():
                    fp.write(chunk)

            fp.close()
            fp = open(tf, 'r')

            try:
                tc.add_torrent(b64encode(fp.read()))
            except transmissionrpc.error.TransmissionError as e:
                if str(e) == 'Query failed with result "duplicate torrent".':
                    pass
                else:
                    raise

            fp.close()
            unlink(tf)
        else:
            for url in request.POST['torrentUrls'].split("\n"):
                try:
                    tc.add_torrent(url)
                except transmissionrpc.error.TransmissionError as e:
                    if str(e)=='Query failed with result "duplicate torrent".':
                        pass
                    else:
                        raise

        return redirect('/')
    else:
        return HttpResponseBadRequest(
            content=dumps({
                'status': 'error',
                'reason': 'Request method should be POST'
            }), content_type='application/json'
        )

@login_required
def api_list(request):
    """
    List all torrents
    """
    filter = request.GET.get('filter', '')
    torrents = Torrent.objects.filter(
        name__icontains=filter).order_by(
        '-created')

    data = []
    for t in torrents:
        data.append({
            'hash': t.hash,
            'name': t.name,
            'status': t.status,
            'progress': t.progress,
            'recheckProgress': t.progress,
        })

    return HttpResponse(
        content=dumps(data),
        content_type='application/json'
    )

def download(request, hardlink):
    """
    Download file with hardlink
    """
    hardlink = get_object_or_404(
        Hardlink,
        token=hardlink,
        created__gte=(datetime.now() - timedelta(
            seconds=settings.HARDLINK_TTL))
    )
    filename = hardlink.file.filename
    view, created = View.objects.get_or_create(
        file=hardlink.file,
        user=hardlink.user
    )

    response = HttpResponse()

    mimetypes.knownfiles.append(
        path.join(
            settings.PROJECT_ROOT,
            '../contrib/mime.types'
        )
    )

    mimetypes.init()

    response['Content-Type'] = mimetypes.guess_type(filename)[0]

    disposition = request.GET.get('disposition', 'attachment')
    basename = path.basename(filename).encode('utf-8')
    if disposition == 'inline':
        response['Content-Disposition'] = 'inline; filename=%s' % \
                                          basename
    else:
        response['Content-Disposition'] = 'attachment; filename=%s' % \
                                          basename

    response['X-Accel-Redirect'] = path.join(
        settings.INTERNAL_DOWNLOAD_PATH,
        filename.encode('utf-8'))

    return response

@login_required
def file(request, file):
    """
    File info page
    """
    file = get_object_or_404(File, pk=file)

    if mimetypes.guess_type(file.filename)[0] != 'video/mp4':
        return redirect(
            path.join(settings.HARDLINK_URL, str(file.pk)) +
            '?redirect=1&disposition=inline')

    return render_to_response(
        'transmission/file.html',
        {
            'file': file,
            'path': settings.HARDLINK_URL
        },
        context_instance=RequestContext(request))

@login_required
def hardlink(request, file):
    """
    Create hardlink to file
    """
    Hardlink.objects.filter(
        created__lte=(datetime.now() - timedelta(
            seconds=settings.HARDLINK_TTL))).delete()

    file = get_object_or_404(File, pk=file)

    token = sha1('%s:%s' % (
        random(),
        file.pk,
    )).hexdigest()

    hardlink = Hardlink(
        token=token,
        file=file,
        user=request.user
    )
    hardlink.save()

    if int(request.GET.get('redirect', 0)) == 1:
        return redirect(
            path.join(
                settings.DOWNLOAD_URL,
                token
            ) + '?' + '&'.join(
                ['%s=%s' % (
                    x, request.GET.get(x)) for x in request.GET.keys()])
        )

    return HttpResponse(
        content=dumps({
            'status': 'ok',
            'token': token,
        }), content_type='application/json'
    )

@login_required
def index(request):
    """
    Index page
    """
    return render_to_response(
        'transmission/list.html',
        {'nav': 'transmission'},
        context_instance=RequestContext(request))

def view_login(request):
    """
    User login view
    """
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                return render_to_response(
                    'transmission/login.html',
                    {'error': 'disabled_account'},
                    context_instance=RequestContext(request))
        else:
            return render_to_response(
                'transmission/login.html',
                {'error': 'invalid_login'},
                context_instance=RequestContext(request))
    else:
        return render_to_response(
            'transmission/login.html',
            context_instance=RequestContext(request))

@login_required
def view_logout(request):
    """
    User logout view
    """
    logout(request)
    return redirect('/')
