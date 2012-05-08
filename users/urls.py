from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^profile/$', views.profile),
#    url(r'^profile/update/(?P<username>\w+)/$', views.update),
#    url(r'^profile/reset-password/(?P<username>\w+)/$', views.reset),
#    url(r'^profile/upload/(?P<username>\w+)/$', views.upload),
)
