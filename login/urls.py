from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
from django.contrib.auth.views import login, logout
import views 

urlpatterns = patterns('',
    url(r'^$', views.public),
    url(r'^public/$', views.public),
    url(r'^login/$', login, {'template_name': 'login/login.html'},
                            name='log-in'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='log-out'),
    url(r'^register/$', views.register),
    
#    url(r'^knock/$', login, {'template': '),
)
