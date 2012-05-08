from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^$', views.public),
    url(r'^create/$', views.create),
)
