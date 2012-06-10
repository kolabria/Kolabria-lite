from django.conf.urls.defaults import include, patterns, url
from django.conf import settings

import views 

urlpatterns = patterns('',
    url(r'^walls/(?P<wid>\w+)/$', views.view),
    url(r'^walls/reset/(?P<box_id>\w+)/$', views.reset_box),
    url(r'^restore/(?P<home_box_id>\w+)/$', views.restore_box),
    url(r'^wikiwall/thank-you/$', views.thank_you),
)
