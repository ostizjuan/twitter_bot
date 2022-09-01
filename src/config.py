import os
import json


def get_config_path():
    return os.path.join(os.getcwd(), 'config.bat')


def dict_to_binary(credentials):
    binary = ' '.join(format(ord(letter), 'b') for letter in credentials)
    return binary


def binary_to_dict(credentials):
    credentials = ''.join(chr(int(x, 2)) for x in credentials.split())
    return json.loads(credentials)


def persisted_config():
    if os.path.exists(get_config_path()):
        with open(get_config_path(), 'rb') as file:
            credentials = file.read()
            return binary_to_dict(credentials)
    else:
        return None


def create_config(username, password):
    with open(get_config_path(), 'wb') as file:
        credentials = json.dumps({'user': username, 'password': password})
        credentials = dict_to_binary(credentials)
        file.write(bytes(credentials.encode('utf-8')))
