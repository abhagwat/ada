from ws4py.client.threadedclient import WebSocketClient as WebSocket

from threading import Thread
import sys

apoorvaURL = '128.237.222.84'
dropletURL = '104.131.112.48'

wsURL = dropletURL
if 'local' in sys.argv:
    wsURL = apoorvaURL

class WSClient(WebSocket):
    
    def opened(self):
        print "We established a connection"

    def received_message(self, message):
        print "We got : ", message

    def closed(self, code, reason=None):
        print "Connection closed booooo!"

wsclient = WSClient("ws://%s:8888/socket" % wsURL)



def establishConnection():
    global wsclient
    while not wsclient:
        pass
    wsclient.connect()
    wsclient.run_forever()

WSThread = Thread(target=establishConnection)
WSThread.daemon = True
WSThread.start()

write = wsclient.send


print "My name"

