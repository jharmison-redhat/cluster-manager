from faros_config import FarosConfig
from flask import request
from werkzeug.utils import secure_filename


def config(config_file: str = 'config') -> FarosConfig:
    if request.args.get('conf') is not None:
        config_file = secure_filename(request.args.get('conf'))
    return FarosConfig.from_yaml('/data/{}.yml'.format(config_file))
