from flask import Flask, redirect, url_for, send_from_directory

from .api import api_bp
from .forms import form_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api')
app.register_blueprint(form_bp, url_prefix='/form')
app.config['SECRET_KEY'] = 'ultra secure'


@app.route('/')
def index():
    return redirect(url_for('config_form.index'))


@app.route('/js/<path:path>')
def send_js(path: str):
    return send_from_directory('static/js', path)


@app.route('/css/<path:path>')
def send_css(path: str):
    return send_from_directory('static/css', path)
