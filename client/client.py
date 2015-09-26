#!/usr/local/bin/python -i

from ws4py.client.threadedclient import WebSocketClient as WebSocket

from threading import Thread
import sys
from time import time, sleep

from subprocess import Popen, PIPE

apoorvaURL = '128.237.222.84'
dropletURL = '104.131.112.48'

wsURL = dropletURL
if 'local' in sys.argv:
    wsURL = apoorvaURL


class SongPlayer(object):
    def __init__(self, filename):
        self.filename = filename

    def startProcess(self):
        self.vlcProcess = Popen(["/Applications/VLC.app/Contents/MacOS/VLC", "-I", "rc", self.filename], stdin=PIPE, stdout=PIPE)

    def sendCommandToProcess(self, input):
        self.vlcProcess.stdin.write(input + '\n')

    def pause(self):
        self.sendCommandToProcess("pause\n")

    def play(self):
        self.sendCommandToProcess("play")

    def seek(self, time):
        # time in seconds
        self.sendCommandToProcess("seek %d\n" % time)

print "Client imported 6"

class WSClient(WebSocket):
    
    def opened(self):
        print "We established a connection"
        self.player = SongPlayer("simarik.mp3")
        self.player.startProcess()
        self.player.pause()
        self.serverPrescription = 0

    def received_message(self, message):
        print "We got : ", message
        # assert message == "play"
        if str(message) == "play":
            print "My UNIX time is ", time()
            self.player.pause()
        elif "seek" in str(message):
            print "Executing ", str(message)
            # self.player.sendCommandToProcess(str(message)+"\n")
            self.player.sendCommandToProcess("get_time")
            self.serverPrescription = int(str(message)[5:])
            print "Server prescription", self.serverPrescription

    def closed(self, code, reason=None):
        print "Connection closed booooo!"

wsclient = WSClient("ws://%s:8888/socket" % wsURL)

print "Client imported 5"

def establishConnection():
    global wsclient
    while not wsclient:
        pass
    wsclient.connect()
    print "RUNNING FOREVER"
    wsclient.run_forever()

WSThread = Thread(target=establishConnection)
WSThread.daemon = True
WSThread.start()

print "Client imported 4"

sleep(1)

write = wsclient.send

print "Client imported 3"

def listenToVLC():
    global wsclient
    print "entered the listener"
    
    while True:
        try:
            pollState = wsclient.player.vlcProcess.poll()
        except:
            continue

        if pollState:
            continue
        line = wsclient.player.vlcProcess.stdout.readline()
        line = line[2:]

        try:
            timestamp = int(line)
            print "The current VLC position is ", timestamp
            if timestamp == wsclient.serverPrescription:
                print "We're in sync"
            else:
                print "Seeking to ", wsclient.serverPrescription
                wsclient.player.seek(wsclient.serverPrescription)

        except:
            pass

print "Client imported 2"


VLCListener = Thread(target=listenToVLC)
VLCListener.daemon = True
VLCListener.start()


print "Client imported 1"





















