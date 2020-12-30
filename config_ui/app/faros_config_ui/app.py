from flask import Flask
from socket import gethostname

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World, from {}!\n'.format(gethostname())
