from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'transmission.views.index'),
    (r'api\/transmission\/list.json', 'transmission.views.api_list'),
    # Examples:
    # url(r'^$', 'blackbox.views.home', name='home'),
    # url(r'^blackbox/', include('blackbox.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
