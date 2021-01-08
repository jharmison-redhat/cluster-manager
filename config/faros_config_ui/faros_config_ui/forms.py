from flask import Blueprint, render_template, request
from ipaddress import ip_network
from pydantic import ValidationError

from faros_config import FarosConfig
from faros_config_ui.form_data.configform import ConfigForm

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
            validated_config = FarosConfig.parse_obj(submitted_config)
            return render_template(
                'validate.html', config=validated_config
            )
        except ValidationError as e:
            return render_template(
                'failed.html', config=submitted_config, error=e
            )
    return render_template('form.html', form=form)
