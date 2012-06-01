# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# STATIC and MEDIA files
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Site Map - Web and mobile devices (urls to views)
# /             public.views.home
# /create       public.views.create
# /devices      appliance.views.devices
# /login        django.contrib.auth.views.login
# /logout       django.contrib.auth.views.logout
# /walls/       walls.views.walls
# /walls/<wid>  walls.views.view
# TODO: appliance views & walls CRUD

urlpatterns = patterns('',
    (r'', include('public.urls')), # / /create/
    (r'', include('login.urls')), # /login/ /logout/ /register/
    (r'', include('appliance.urls')), # /devices/ 
    (r'', include('walls.urls')), # /wall/
    (r'', include('upload.urls')), # /upload/
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
