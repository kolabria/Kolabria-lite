from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^create/$', views.create),
    url(r'^welcome/$', views.welcome),
    url(r'^account/add/$', views.create),
)
