from django.conf.urls import patterns, include, url
from views import *
from sell.views import *
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
    
    url(r'^landing/$',landing),
    # url(r'^mailTemplate/$',mail_template),
    # url(r'^send_mail/$',send_maill),
    url(r'^$', landing),
    url('^anasayfa/$',anasayfa),
    url('^admin_panel/$',admin_panel),

    url('^reset_data/$',reset_data),
    
    #sell
    url('^bilet_ilan/$',bilet_ilan),
    url('^bilet_detaylari/$',bilet_detaylari),
    url('^fiyatlandir/$',fiyatlandir),
    url('^teslimat/$',teslimat),
    url('^onayla/$',onayla),
)
