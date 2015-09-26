
from flask import *
import requests

hackyServer = Flask(__name__)

@hackyServer.route('/hack')
def hack():
    import client
    client.write("play")

if __name__=='__main__':
    hackyServer.run(port=80, host='0.0.0.0', debug=True)


