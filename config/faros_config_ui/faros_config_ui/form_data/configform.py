from flask_wtf import FlaskForm
from wtforms import (
    FormField,
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


# TODO: Add validators that use pydantic checking and produce verbose errors on
# the forms.

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


class NetworkForm(FlaskForm):
    """Networking configuration form"""
    port_forward = MultiCheckboxField(
        'Services',
        [],
        choices=[
            double_str('SSH to Bastion'),
            double_str('HTTPS to Cluster API'),
            double_str('HTTP to Cluster Apps'),
            double_str('HTTPS to Cluster Apps'),
            double_str('HTTPS to Cockpit Panel'),
        ],
        description=('Select the services that should be forwarded through the'
                     " bastion's gateway.")
    )
    subnet = StringField(
        'Subnet',
        [validators.required()],
        default='192.168.8.0/24',
        description=('Enter the subnet to use for the FarosLAN network in CIDR'
                     ' notation.')
    )
    interfaces = MultiCheckboxField(
        'Interfaces',
        [validators.required()],
        choices=[double_str('eno{}'.format(num + 1)) for num in range(5)],
        description=('Select the bastion interfaces to place on the FarosLAN'
                     ' network.')
    )
    dns_forward_resolvers = TextAreaField(
        'Upstream DNS',
        description=('Enter a newline-delimited list of all upstream DNS'
                     ' resolvers you would like to use, if different than'
                     ' those from the WAN DHCP.')
    )


class SecretsForm(FlaskForm):
    """Secret configuration form"""
    become_pass = PasswordField(
        'Sudo password',
        [validators.required()],
        description=('Enter the password required to sudo as your'
                     ' administrative user on the bastion host.')
    )
    pull_secret = PasswordField(
        'Pull secret',
        [validators.required()],
        description=('Enter your pull secret, acquired from '
                     'https://cloud.redhat.com.')
    )


class ManagementForm(FlaskForm):
    """Management provider configuration form"""
    management_provider = SelectField(
        'Provider',
        [validators.required()],
        choices=[('ilo', 'iLO',)],
        description='Select management provider type.'
    )
    management_username = StringField(
        'Username',
        [validators.required()],
        description='Enter your management provider user name.'
    )
    management_password = PasswordField(
        'Password',
        [validators.required()],
        description='Enter your management provider password.'
    )


class ProxyForm(FlaskForm):
    """Proxy configuration form"""
    proxy_http = StringField(
        'HTTP',
        description='Enter the proxy HTTP endpoint'
    )
    proxy_https = StringField(
        'HTTPS',
        description='Enter the proxy HTTPS endpoint'
    )
    noproxy = TextAreaField(
        'Ignore',
        description=('Enter a newline-delimited list of the websites that'
                     ' should bypass the proxy.')
    )
    proxy_ca = TextAreaField(
        'CA',
        description=('Enter the full Certificate Authority for the HTTPS'
                     'proxy in PEM format.')
    )


class ConfigForm(FlaskForm):
    """Faros Configuration Form"""
    network = FormField(
        NetworkForm,
        description='Configuration of the FarosLAN Network'
    )
    secrets = FormField(
        SecretsForm,
        description='Configuration of secrets necessary for Faros deployment'
    )
    management = FormField(
        ManagementForm,
        description='Configuration of the Management Provider for nodes'
    )
    proxy = FormField(
        ProxyForm,
        description='Configuration of an outbound HTTP/S proxy'
    )
    submit = SubmitField('Submit')
