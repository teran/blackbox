from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'transmission.views.index'),
    (r'^api\/transmission\/filter$', 'transmission.views.api_filter'),
    (r'^api\/transmission\/list$', 'transmission.views.api_list'),
    (r'^api\/transmission\/add$', 'transmission.views.api_add_torrent'),
    (r'^api\/transmission\/(?P<hash>[0-9a-f]{40})\/' +
     '(?P<action>start|stop|delete|info|verify)$',
     'transmission.views.api_action')
)
