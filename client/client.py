from ws4py.client.threadedclient import WebSocketClient as WebSocket

from threading import Thread

class WSClient(WebSocket):
    
    def opened(self):
        print "We established a connection"

    def received_message(self, message):
        print "We got : ", message

    def closed(self):
        print "Connection closed booooo!"

wsclient = WSClient("ws://104.131.112.48:8888/socket")



def start():
    global wsclient
    while not wsclient:
        pass
    wsclient.connect()
    wsclient.run_forever()

WSThread = Thread(target=start)
WSThread.run()

write = wsclient.send

