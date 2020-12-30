from flask import Flask, redirect, url_for
from flask_bootstrap import Bootstrap

from .api import api
from .forms import form_bp

app = Flask(__name__)
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(form_bp, url_prefix='/form')
app.config['SECRET_KEY'] = 'ultra secure'
Bootstrap(app)


@app.route('/')
def index():
    return redirect(url_for('config_form.index'))
