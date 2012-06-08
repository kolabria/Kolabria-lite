from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from appliance import views

urlpatterns = patterns('',
    url(r'^devices/$', views.appliances),
    url(r'^devices/edit/(?P<box_id>\w+)/$', views.detail),
    url(r'^devices/remove/(?P<box_id>\w+)/$', views.remove_box),
    url(r'^devices/reset/(?P<bid>\w+)/$', views.reset),
    url(r'^devices/(?P<box_id>\w+)/unshare/(?P<shared_id>\w+)/$', views.unshare_box),
    url(r'^box/$', views.auth_box),
    url(r'^host/$', views.auth_host),
    url(r'^receiver/$', views.auth_receiver),
    url(r'^box/(?P<bid>\w+)/$', views.the_box),
    url(r'^appliances/$', views.appliances),
    url(r'^wikiwall/(?P<box_id>\w+)/$', views.wikiwall),
    url(r'^host/wikiwall/(?P<box_id>\w+)/$', views.host_wall), 
    url(r'^receiver/wikiwall/(?P<host_id>\w+)/$', views.receiver_wall),
    url(r'^connect/(?P<host_id>\w+)/$', views.connect2host),
)
