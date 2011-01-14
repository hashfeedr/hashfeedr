import os, sys
sys.path.append('/home/deploy/apps/hashfeedr/djangostuff')
sys.path.append('/home/deploy/apps/hashfeedr')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
