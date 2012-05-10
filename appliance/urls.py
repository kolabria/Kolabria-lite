from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from appliance import views

urlpatterns = patterns('',
    url(r'^devices/$', views.appliances),
    url(r'^devices/remove/(?P<bid>\w+)/$', views.remove_box),
    url(r'^box/$', views.auth_box),
    url(r'^box/(?P<bid>\w+)/$', views.the_box),
    url(r'^box/active/(?P<wid>\w+)/$', views.active_wall),
    url(r'^box/unsubwall/(?P<bid>\w+)/$', views.unsubwall),
    url(r'^box/pubwall/(?P<bid>\w+)/$', views.pubwall),
    url(r'^appliances/$', views.appliances),
)
