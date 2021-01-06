from flask_wtf import FlaskForm
from wtforms import (
    SelectField,
    SubmitField
)
from wtforms.validators import DataRequired
from flask import Blueprint, redirect, render_template, url_for


class ConfigForm(FlaskForm):
    """Faros Configuration Form"""
    port_forward = SelectField(
        'Services to Enable',
        [DataRequired()],
        choices=[
            ('SSH to Bastion', 'SSH to Bastion'),
            ('HTTPS to Cluster API', 'HTTPS to Cluster API'),
            ('HTTP to Cluster Apps', 'HTTP to Cluster Apps'),
            ('HTTPS to Cluster Apps', 'HTTPS to Cluster Apps'),
            ('HTTPS to Cockpit Panel', 'HTTPS to Cockpit Panel'),
        ]
    )
    submit = SubmitField('Submit')


form_bp = Blueprint('config_form', __name__, template_folder='templates')


@form_bp.route('/', methods=['GET', 'POST'])
def form():
    form = ConfigForm()
    if form.validate_on_submit():
        return redirect(url_for('config_form.validate'))
    return render_template(
        'form.html',
        form=form
    )


@form_bp.route('/validate')
def validate():
    return render_template('validate.html')
