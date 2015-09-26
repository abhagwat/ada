
# from tornado import *
from tornado.websocket import WebSocketHandler
import tornado
import tornado.web
from tornado.ioloop import PeriodicCallback

import simplejson as json
import uuid

class WSHandler(WebSocketHandler):
    connections = {}
    masterClientID = None
    time_counter = 0

    def check_origin(self, origin):
        return True

    def open(self):
        print "WebSocket opened"
        self.uniqueID = str(uuid.uuid4())[:8]

        if self.connections == {}: # This is the first connection
            self.masterClientID = self.uniqueID
        self.connections[self.uniqueID] = self

    def on_message(self, message):
        print "Mesij : ", message

        if self.uniqueID != self.masterClientID:
            print "Non-master message received, ignoring"
            return

        for connection in self.connections.values():
            connection.write_message("play")
        periodicCallback = PeriodicCallback(self.send_sync_messages, 500)
        periodicCallback.start()

        # for connID, connection in self.connections.items():
        #     if connID != self.uniqueID:
        #         connection.write_message(self.uniqueID + " : " + message)

    def on_close(self):
        print "Connection closed"

    def send_sync_messages(self):
        for connection in self.connections.values():
            connection.write_message("seek %d" % self.time_counter)
        self.time_counter += 1


app = tornado.web.Application([
        (r"/socket", WSHandler)
    ])

if __name__ == "__main__":
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()

