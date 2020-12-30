from flask import Flask
from socket import gethostname

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, WORLD, from {}!\n'.format(gethostname())
