
from flask import *
import requests

hackyServer = Flask(__name__)

@hackyServer.route('/hack')
def hack():
    import client

