
from flask import *
import requests
import client

hackyServer = Flask(__name__)

@hackyServer.route('/hack')
def hack():
    client.write("play")
    return "Playing!"

if __name__=='__main__':
    hackyServer.run(port=8000, host='0.0.0.0', debug=True)


