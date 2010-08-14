from twisted.internet import reactor, task
from twisted.application import service
from txwebsockets import WebSocketFactory, BasicOperations
import datetime

class HashConnector(BasicOperations):
    def on_connect(self):
        self.timer = task.LoopingCall(self.write_something)
        self.timer.start(0.1)

    def on_close(self, r):
        self.timer.stop()

    def write_something(self):
        self._out("%s" % datetime.datetime.now())

    def on_read(self, line):
        pass

hc = HashConnector()
factory = WebSocketFactory(hc)
application = service.Application("hashfeedr")
reactor.listenTCP(8338, factory)
