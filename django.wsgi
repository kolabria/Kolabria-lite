import os
import sys
import site

sys.path.append('/srv/Kolabria-lite')
sys.path.append('/srv')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
