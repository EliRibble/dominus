import os
import yaml

DEFAULTS = {
    'db' : "postgres://dev:development@localhost:5432/dominus",
}

def get():
    if get.config:
        return get.config
    config = DEFAULTS.copy()
    with open('/etc/dominus.yaml', 'r') as f:
        data = yaml.load(f)
    config.update(data)
    get.config = config
    return config
get.config = None
