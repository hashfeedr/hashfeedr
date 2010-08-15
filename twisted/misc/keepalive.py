from twisted.internet import reactor, task, protocol, defer
from twisted.python import log

class KeepAlive(object):
    @classmethod
    def attach(klass,fn,interval=30):
        return klass(fn,interval)

    def __init__(self,fn,interval):
        self.fn = fn
        self.task = task.LoopingCall(self.keepalive)
        self.task.start(interval)

    @defer.inlineCallbacks
    def keepalive(self):
        log.msg("%s: Keepalive ping" % repr(self))
        yield self.fn()
