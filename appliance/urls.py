from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from appliance import views

urlpatterns = patterns('',
    url(r'^devices/$', views.appliances),
    url(r'^devices/edit/(?P<box_id>\w+)/$', views.detail),
    url(r'^devices/remove/(?P<bid>\w+)/$', views.remove_box),
    url(r'^devices/reset/(?P<bid>\w+)/$', views.reset),
    url(r'^devices/(?P<bid>\w+)/unshare/(?P<shared_id>\w+)/$', views.unshare_box),
    url(r'^box/$', views.auth_box),
    url(r'^box/(?P<bid>\w+)/$', views.the_box),
    url(r'^appliances/$', views.appliances),
    url(r'^wikiwall/(?P<box_id>\w+)/$', views.wikiwall),
)
