# an object of WSGI application
from flask import Flask, redirect, url_for, request, jsonify
import requests

app = Flask(__name__)  # Flask constructor


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


@app.route('/test', methods=['POST'])
def test():
    # handle the POST request
    if request.method == 'POST':
        print(request.get_json())
        return "shit"


def runServer(port):
    app.run(port=port)


def post(port, route, json):
    r = requests.post('http://localhost:'+str(port)+route, json=json)
    return r


def get(port, route):
    r = requests.get('http://localhost:'+str(port)+route)
    return r

