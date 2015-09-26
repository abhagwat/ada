from ws4py.websocket import WebSocket

from threading import Thread

class WSClient(WebSocket):
    
    def opened(self):
        print "We established a connection"

    def received_message(self, message):
        print "We got : ", message

    def closed(self):
        print "Connection closed booooo!"

wsclient = WSClient()

def start():
    wsclient.run()

WSThread = Thread(target=start)
WSThread.run()

write = wsclient.send

