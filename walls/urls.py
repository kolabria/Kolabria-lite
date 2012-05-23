from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^walls/$', views.walls),
    url(r'^walls/create/$', views.create),
    url(r'^walls/(?P<wid>\w+)/$', views.view),
    url(r'^walls/reset/(?P<box_id>\w+)/$', views.reset_box),
#    url(r'^wikiwall/(?P<box_id>\w+)/$', views.wikiwall),
)
