import os
import time
import json

import PySimpleGUI as sg

from src.tweet import Tweet


def persisted_config():
    try:
        with open(os.path.join(os.getcwd(), 'config.json'), 'r') as fp:
            return json.load(fp)
    except:
        return None

def create_config(username, password):
    with open(os.path.join(os.getcwd(), 'config.json'), 'w') as fp:
        fp.write(json.dumps({'user':username, 'password':password}))

def main_window():
    config = persisted_config()

    layout = []

    if config:
        layout.append([
            [sg.Text(f'User: {config["user"]}'), sg.Button('Edit', key='-EDIT-'), sg.Text('Timer'), sg.Spin([i for i in range(1,86400)], key='-TIMER-', size=(5, 1), initial_value=1)],
            [sg.Text('Tweet content')],
            [sg.Multiline('', key='-MT-', size=(45, 5), write_only=True)],
            [sg.Button('Start', key='-START-'), sg.Button('Stop', key='-STOP-')]
        ])

    else:
        layout.append([
            [sg.Text('User:', size=(10, 1)), sg.Input(key='-USERNAME-')],
            [sg.Text('Password:', size=(10, 1)), sg.Input(key='-PASSWORD-', password_char='*')],
            [sg.Button('ADD', key='-ADD-')]
        ])

    tweet = Tweet()
    window = sg.Window('Tweet', layout=layout)
    while True:
        event, values = window.read(timeout=10)
        if tweet.timer.check_interval():
            tweet.push_tweet()

        elif event == sg.WIN_CLOSED:
            break

        elif event == '-ADD-':
            create_config(values['-USERNAME-'], values['-PASSWORD-'])
            window.close()
            return True
        
        elif event == '-START-':
            tweet.login(config['user'], config['password'])
            tweet.push_tweet()
        
        elif event == '-STOP-':
            tweet.stop()

        elif event == '-EDIT-':
            window.close()
            os.remove(os.path.join(os.getcwd(), 'config.json'))
            main_window()

def start():
    if(main_window()):
        main_window()