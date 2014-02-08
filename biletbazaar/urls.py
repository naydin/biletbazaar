from django.conf.urls import patterns, include, url
from views import *
from sell.views import *
from buy.views import *
from forms import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



from django.template.loader import add_to_builtins
for tag in settings.AUTOLOAD_TEMPLATETAGS:
    add_to_builtins(tag)

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
    
    #buy
    url('^biletal1/$',biletal1),
    url('^biletal2/$',biletal2),
    url('^biletal3/$',biletal3),
    url('^biletal4/$',biletal4),
    
    #event group
    url('^event_group/$',event_group),
    url('^event/$',event),
    
    url(r'^login/$',login_user),
    url(r'^logout/$',logout_view),
    
    url('^bize_ulasin/$',bize_ulasin),
    url('^hesabim/$',hesabim),
    url('^search_result/$',search_result),
)
