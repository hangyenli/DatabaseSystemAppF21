# an object of WSGI application
from flask import Flask

app = Flask(__name__)  # Flask constructor


# A decorator used to tell the application
# which URL is associated function
@app.route('/')
def hello():
    return 'HELLO'


def runServer(port):
    app.run(port=port)

