import ipaddress
import json
from pydantic import BaseModel
from typing import Optional
import yaml

from .network import NetworkConfig
from .bastion import BastionConfig
from .cluster import ClusterConfig
from .proxy import ProxyConfig


class PydanticEncoder(json.JSONEncoder):
    def default(self, obj):
        obj_has_dict = getattr(obj, "dict", False)
        if obj_has_dict and callable(obj_has_dict):
            return obj.dict(exclude_none=True)
        elif isinstance(obj, ipaddress._IPAddressBase):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


class FarosConfig(BaseModel):
    network: NetworkConfig
    bastion: BastionConfig
    cluster: ClusterConfig
    proxy: Optional[ProxyConfig]

    @classmethod
    def from_yaml(cls, yaml_file: str) -> 'FarosConfig':
        with open(yaml_file) as f:
            config = yaml.safe_load(f)

        return cls.parse_obj(config)

    def to_json(self) -> str:
        return json.dumps(self, sort_keys=True, indent=4,
                          separators=(',', ': '), cls=PydanticEncoder)
