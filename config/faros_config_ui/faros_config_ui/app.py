from flask import Flask, jsonify
from faros_config import FarosConfig

app = Flask(__name__)


@app.route('/health')
def health():
    try:
        _ = FarosConfig.from_yaml('/data/config.yml')
        return jsonify({'health': 'ok'})
    except:  # noqa: E722
        return jsonify({'health': 'bad'})


@app.route('/config')
def config():
    config = FarosConfig.from_yaml('/data/config.yml')
    return config.to_json()
