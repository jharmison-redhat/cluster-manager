from flask_wtf import FlaskForm
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
from typing import Tuple


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


# TODO: Add validators that use pydantic checking and produce verbose errors on
# the form.
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
    subnet = StringField(
        'FarosLAN Subnet',
        [validators.required()],
        default='192.168.8.0/24'
    )
    interfaces = MultiCheckboxField(
        'Interfaces to include on FarosLAN bridge',
        [validators.required()],
        choices=[double_str('eno{}'.format(num + 1)) for num in range(5)]
    )
    dns_forward_resolvers = TextAreaField(
        'List of forwarding DNS resolvers'
    )
    become_pass = PasswordField(
        'Sudo password for your bastion user',
        [validators.required()]
    )
    pull_secret = PasswordField(
        'Pull secret from cloud.redhat.com',
        [validators.required()]
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
