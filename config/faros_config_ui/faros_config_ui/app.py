from flask import Flask, jsonify

from .config import config

app = Flask(__name__)


@app.route('/')
def redirect():
    return jsonify({'allowed_urls': ['/health', '/config']})


@app.route('/health')
def health():
    try:
        _ = config().to_json()
        return jsonify({'health': 'ok'})
    except Exception as e:
        return jsonify({'health': 'bad', 'message': str(e)})


@app.route('/config')
def get_config():
    return config().to_json()
