from django.conf.urls import patterns, include, url
from views import *
from forms import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'biletbazaar.views.home', name='home'),
    # url(r'^biletbazaar/', include('biletbazaar.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^hello/$', hello),
    url(r'^eventgroups/$', event_groups),
    url(r'^landing/$', landing),
)
