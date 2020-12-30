from faros_config import FarosConfig
from flask import request
from werkzeug.utils import secure_filename


def clean_config_file(config_file: str = 'config') -> str:
    if request.args.get('conf') is not None:
        return secure_filename(request.args.get('conf'))
    elif 'yaml' in request.files:
        return secure_filename(request.files['yaml'].filename)
    else:
        return config_file


def config() -> FarosConfig:
    return FarosConfig.from_yaml('/data/{}.yml'.format(clean_config_file()))


def schema_json() -> str:
    return FarosConfig.schema_json(indent=4)


def raw_config(obj) -> FarosConfig:
    return FarosConfig.from_obj(obj)
