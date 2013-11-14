from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'transmission.views.index'),
    (r'^api\/transmission\/list', 'transmission.views.api_list'),
    (r'^api\/transmission\/add$', 'transmission.views.api_add_torrent'),
    (r'^api\/transmission\/(?P<id>[0-9]+)\/' +
     '(?P<action>start|stop|delete|info|verify)$',
     'transmission.views.api_action'),

    # Examples:
    # url(r'^$', 'blackbox.views.home', name='home'),
    # url(r'^blackbox/', include('blackbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
