import os
import time
import multiprocessing

import PySimpleGUI as sg

from src.tweet import Tweet
from src.config import persisted_config, create_config, get_config_path


def get_layout(config):
    """ Obtain the layout for the main window, based on whether or not the user has a config file """
    layout = []

    if config is not None:
        layout.append([
            [sg.Text(f'User: {config["user"]}'), sg.Button('Edit', key='-EDIT-'), sg.Text('Timer'),
                sg.Spin([i for i in range(1, 86400)], key='-TIMER-', size=(5, 1), initial_value=1)],
            [sg.Text('Tweet content')],
            [sg.Multiline('', key='-MT-', size=(45, 5), write_only=True)],
            [sg.Button('Start', key='-START-'),
                sg.Button('Stop', key='-STOP-')]
        ])

    else:
        layout.append([
            [sg.Text('User:', size=(10, 1)), sg.Input(key='-USERNAME-')],
            [sg.Text('Password:', size=(10, 1)), sg.Input(
                key='-PASSWORD-', password_char='*')],
            [sg.Button('ADD', key='-ADD-')]
        ])

    return layout


def make_tweet(tweet, config):
    if not tweet.logged:
        tweet.login(config['user'], config['password'])
    tweet.push_tweet()


def main_window():
    """ Main window """
    config = persisted_config()
    layout = get_layout(config)

    tweet = Tweet()

    window = sg.Window('Tweet', layout=layout)
    while True:
        event, values = window.read(timeout=10)
        if tweet.timer.check_interval():
            tweet.push_tweet()

        else:
            match event:
                case sg.WIN_CLOSED:
                    break
                case '-ADD-':
                    if values['-USERNAME-'] and values['-PASSWORD-']:
                        create_config(values['-USERNAME-'],
                                      values['-PASSWORD-'])
                        window.close()
                        main_window()
                case '-START-':
                    push_tweet = multiprocessing.Process(
                        target=make_tweet, args=(tweet, config))
                    push_tweet.start()
                case '-STOP-':
                    tweet.stop()
                    push_tweet.terminate()
                case '-EDIT-':
                    window.close()
                    os.remove(get_config_path())
                    main_window()


def start():
    main_window()
