from flask import Blueprint, jsonify, request, url_for
import os
from pydantic import ValidationError
import yaml

from .config import clean_config_file, config, raw_config, schema_json

api_bp = Blueprint('config_api', __name__, template_folder='templates')


@api_bp.route('/')
def index():
    allowed_urls = [
        'health',
        'config',
        'config/schema'
    ]
    allowed_urls.sort()
    return jsonify({
        'allowed_urls': [
            '{}{}'.format(url_for('config_api.index'), url)
            for url in allowed_urls
        ]
    })


@api_bp.route('/health')
def health():
    try:
        _ = config().to_json()
        return jsonify({'health': 'ok'})
    except ValidationError as e:
        return jsonify({'health': 'bad', 'validation_errors': e.errors()})
    except Exception as e:
        return jsonify({'health': 'bad', 'message': str(e)})


@api_bp.route('/config')
def get_config():
    return config().to_json()


@api_bp.route('/config', methods=['POST'])
def post_config():
    if 'yaml' in request.files:
        new_config_file = request.files['yaml']
        new_config_obj = yaml.safe_loads(new_config_file)
        try:
            validated_config = raw_config(new_config_obj)
        except ValidationError as e:
            return jsonify({'status': 'failed',
                            'validation_errors': e.errors()})
        validated_path = os.path.join('/data', clean_config_file())
        new_config_file.save(validated_path)
        return jsonify({'status': 'saved',
                        'config': validated_config.dict(),
                        'path': validated_path})
    else:
        return jsonify({'status': 'no file'})


@api_bp.route('/config/schema')
def schema():
    return schema_json()
