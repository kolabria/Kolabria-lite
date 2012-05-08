from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^walls/$', views.walls),
    url(r'^walls/create/$', views.create),
    url(r'^walls/share/(?P<wid>\w+)/$', views.share),
    url(r'^walls/unshare/(?P<wid>\w+)/$', views.unshare),
    url(r'^walls/unpublish/(?P<wid>\w+)/$', views.unpublish),
    url(r'^walls/publish/(?P<wid>\w+)/$', views.publish),
    url(r'^walls/update/(?P<wid>\w+)/$', views.update),
    url(r'^walls/delete/(?P<wid>\w+)/$', views.delete),
    url(r'^walls/(?P<wid>\w+)/$', views.view),
)
