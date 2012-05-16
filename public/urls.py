from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^$', views.public),
    url(r'^home$', views.home),
    url(r'^join/$', views.join),
)
