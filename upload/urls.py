from django.conf.urls.defaults import include, patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

#from upload import views

urlpatterns = patterns('',
    url(r'^upload/$', 'upload.views.upload_file'),
    url(r'^uploaded/$', 'upload.views.uploaded'),
)
