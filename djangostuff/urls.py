import os
import settings
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^djangostuff/', include('djangostuff.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),

	(r'^$', 'hashfeedr.views.landing_page'),
	(r'^feed/((\w|\d|#|\s|\.)+)$', 'hashfeedr.views.feeder'),
	(r'^gofeed$','hashfeedr.views.gofeed'),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__),'..','media')}),
)

