import sys
import os

from datetime import datetime
from twisted.application import internet, service
from twisted.web import server, resource, wsgi, static
from twisted.python import threadpool
from twisted.internet import reactor, task

# env setup for django app
sys.path.append('djangostuff');
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangostuff.settings'
from django.core.handlers.wsgi import WSGIHandler

def wsgi_resource():
        pool = threadpool.ThreadPool()
        pool.start()
        reactor.addSystemEventTrigger('after','shutdown',pool.stop)
        wsgi_resource = wsgi.WSGIResource(reactor,pool,WSGIHandler())
        return wsgi_resource

class TransparentWSGIResource(resource.Resource):
    def __init__(self,wsgi):
        resource.Resource.__init__(self)
        self.wsgi = wsgi

    # This method is called when no static resource is able to handle
    # the request. So, always returns the WSGI resource.
    def getChild(self,path,request):
        # Don't consume request segments - this should be transparent!
        request.postpath.insert(0, request.prepath.pop())
        return self.wsgi

# setup django root resource
root = TransparentWSGIResource(wsgi_resource())

# serve static files from public
media = static.File(os.path.join(os.path.abspath("."), "media"))
root.putChild("media",media)

# serve websocket requests at /time
site = server.Site(root)

# go, go, go
application = service.Application("hashfeedrapp")
internet.TCPServer(8001,site).setServiceParent(application)
