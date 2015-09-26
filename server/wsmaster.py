
# from tornado import *
from tornado.websocket import WebSocketHandler
import tornado
import tornado.web

import simplejson as json
import uuid

class WSHandler(WebSocketHandler):
    connections = {}

    def check_origin(self, origin):
        return True

    def open(self):
        print "WebSocket opened"
        self.uniqueID = str(uuid.uuid4())[:8]
        self.connections[self.uniqueID] = self

    def on_message(self, message):
        print "Mesij : ", message
        for connID in self.connections:
            if connID != self.uniqueID:
                self.write_message(self.uniqueID + " : " + message)

    def on_close(self):
        print "Connection closed"


app = tornado.web.Application([
        (r"/socket", WSHandler)
    ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

