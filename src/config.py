import os
import json


def get_config_path():
    return os.path.join(os.getcwd(), 'config.bat')


def persisted_config():
    if os.path.exists(get_config_path()):
        with open(get_config_path(), 'rb') as file:
            data = file.read()
            return json.loads(data)
    else:
        return None


def create_config(username, password):
    with open(get_config_path(), 'wb') as file:
        data = json.dumps({'user': username, 'password': password})
        file.write(data)
