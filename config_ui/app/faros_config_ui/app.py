import yaml
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('/data/config.yml') as f:
        return jsonify(yaml.safe_load(f))
