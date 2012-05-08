# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# STATIC and MEDIA files
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    (r'', include('public.urls')),
    (r'', include('appliance.urls')),
    (r'', include('login.urls')),
    (r'', include('walls.urls')),
    (r'^blog', include('apps.blog.urls')),
    (r'', include('appliance.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
