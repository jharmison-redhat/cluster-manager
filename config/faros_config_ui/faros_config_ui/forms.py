from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from ipaddress import ip_network
from pydantic import ValidationError
from typing import Tuple
from wtforms import (
    PasswordField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    StringField,
    TextAreaField,
    validators,
    widgets
)

from faros_config import FarosConfig


def double_str(item: str) -> Tuple[str, str]:
    return (item, item,)


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# TODO: Add validators that use pydantic checking and produce verbose errors on the form
class ConfigForm(FlaskForm):
    """Faros Configuration Form"""
    port_forward = MultiCheckboxField(
        'Services to Enable',
        [],
        choices=[
            double_str('SSH to Bastion'),
            double_str('HTTPS to Cluster API'),
            double_str('HTTP to Cluster Apps'),
            double_str('HTTPS to Cluster Apps'),
            double_str('HTTPS to Cockpit Panel'),
        ]
    )
    subnet = StringField('FarosLAN Subnet', [validators.required()])
    interfaces = MultiCheckboxField(
        'Interfaces to include on FarosLAN bridge',
        [validators.required()],
        choices=[double_str('eno{}'.format(num + 1)) for num in range(5)]
    )
    dns_forward_resolvers = TextAreaField(
        'List of forwarding DNS resolvers'
    )
    become_pass = StringField(
        'Sudo password for your bastion user',
        [validators.required()]
    )
    pull_secret = PasswordField(
        'Pull secret from cloud.redhat.com',
        [validators.required()],
        widget=widgets.TextArea()
    )
    management_provider = SelectField(
        'Node Management Provider',
        [validators.required()],
        choices=[('ilo', 'iLO',)]
    )
    management_username = StringField(
        'Username for Management Provider',
        [validators.required()]
    )
    management_password = PasswordField(
        'Password for Management Provider',
        [validators.required()]
    )
    proxy_http = StringField(
        'Proxy HTTP endpoint'
    )
    proxy_https = StringField(
        'Proxy HTTPS endpoint'
    )
    noproxy = TextAreaField(
        'List of sites to ignore proxy settings'
    )
    proxy_ca = TextAreaField(
        'Proxy Certificate Authority PEM text'
    )
    submit = SubmitField('Submit')


form_bp = Blueprint('config_form', __name__, template_folder='templates')


@form_bp.route('/', methods=['GET', 'POST'])
def form():
    form = ConfigForm()
    if request.method == 'POST':
        submitted_config = {
            'network': {
                'port_forward': form.port_forward.data,
                'lan': {
                    'subnet': ip_network(form.subnet.data),
                    'interfaces': form.interfaces.data,
                    'dns_forward_resolvers': [
                        resolver.strip() for resolver in
                        form.dns_forward_resolvers.data.split('\n')
                        if resolver.strip() != ''
                    ],
                    'dhcp': {
                        'ignore_macs': [],  # needs finished
                        'extra_reservations': []  # needs finished
                    }
                }
            },
            'bastion': {
                'become_pass': form.become_pass.data
            },
            'cluster': {
                'pull_secret': form.pull_secret.data,
                'management': {
                    'provider': form.management_provider.data,
                    'user': form.management_username.data,
                    'password': form.management_password.data,
                },
                'nodes': []  # needs finished
            },
            'proxy': {
                'http': form.proxy_http.data,
                'https': form.proxy_https.data,
                'noproxy': [
                    address.strip() for address in
                    form.noproxy.data.split('\n')
                    if address.strip() != ''
                ],
                'ca': form.proxy_ca.data
            }
        }
        try:
            return render_template(
                'validate.html', config=FarosConfig.parse_obj(submitted_config)
            )
        except ValidationError as e:
            return render_template(
                'failed.html', config=submitted_config, error=e
            )
    return render_template('form.html', form=form)
