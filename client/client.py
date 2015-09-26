#!/usr/local/bin/python -i

from ws4py.client.threadedclient import WebSocketClient as WebSocket

from threading import Thread
import sys

from subprocess import Popen, PIPE

apoorvaURL = '128.237.222.84'
dropletURL = '104.131.112.48'

wsURL = dropletURL
if 'local' in sys.argv:
    wsURL = apoorvaURL

class WSClient(WebSocket):
    
    def opened(self):
        print "We established a connection"
        self.player = SongPlayer("simarik.mp3")

    def received_message(self, message):
        print "We got : ", message
        # assert message == "play"
        self.player.startProcess()

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


class SongPlayer(object):
    def __init__(self, filename):
        self.filename = filename

    def startProcess(self):
        self.vlcProcess = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "rc", self.filename], stdin=PIPE)

    def sendCommandToProcess(self, input):
        self.vlcProcess.communicate(input=input)

    def pause(self):
        self.sendCommandToProcess("pause")

    def play(self):
        self.sendCommandToProcess("play")

    def seek(self, time):
        # time in seconds
        self.sendCommandToProcess("seek %d" %time)




















