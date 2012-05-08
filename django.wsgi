import os
import sys
import site

site.addsitedir('/srv/kolabria-app/venv16/lib/python2.6/site-packages')

sys.path.append('/srv/kolabria-app')
sys.path.append('/srv')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
