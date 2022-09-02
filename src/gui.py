import os
from random import choice

import PySimpleGUI as sg

from src.timer import Timer
from src.tweet import Tweet
from src.config import persisted_config, create_config, get_config_path
from src.db import get_tweets, add_tweet


def add_tweet_window(username):
    window = sg.Window('Add Tweet', layout=[
        [sg.Text('Message:')],
        [sg.InputText(key='msg')],
        [sg.Button('Add Tweet')]
    ])

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            break
        elif event == 'Add Tweet':
            add_tweet(values['msg'], username)
            window.close()
            break


def get_random_tweet(tweets):
    """ Get a random tweet from the database """
    return choice(tweets)


def get_layout(config, tweets=None):
    """ Obtain the layout for the main window, based on whether or not the user has a config file """
    layout = []

    if config is not None:
        layout.append([
            [sg.Text(f'User: {config["user"]}'), sg.Button('Edit', key='-EDIT-'), sg.Text('Timer (Minutes)'),
                sg.Spin([i for i in range(1, 1440)], key='-TIMER-', size=(5, 1), initial_value=1)],
            [sg.Text('Tweet content')],
            [sg.Multiline('\n'.join([f'{tweet[0]}: {tweet[1]}' for tweet in tweets]),
                          key='-MT-', size=(45, 5), disabled=True)],
            [sg.Button('Start', key='-START-'),
                sg.Button('Stop', key='-STOP-'),
                sg.Button('Add Tweet', key='-ADD_TWEET-', size=(10, 1))]
        ])

    else:
        layout.append([
            [sg.Text('User:', size=(10, 1)), sg.Input(key='-USERNAME-')],
            [sg.Text('Password:', size=(10, 1)), sg.Input(
                key='-PASSWORD-', password_char='*')],
            [sg.Button('ADD', key='-ADD-')]
        ])

    return layout


def make_tweet(tweet, config, timer):
    tweet.login(config['user'], config['password'])
    tweet.push_tweet()
    timer.start()
    tweet.logged = False
    tweet.stop()


def main_window():
    """ Main window """
    config = persisted_config()

    if config is None:
        layout = get_layout(config)
    else:
        tweets = get_tweets(config['user'])
        layout = get_layout(config, tweets)

    timer = Timer()
    tweet = Tweet()

    window = sg.Window('Tweet', layout=layout)
    while True:
        event, values = window.read(timeout=10)

        if timer.check_interval():
            make_tweet(tweet, config, timer)
        else:
            match event:
                case sg.WIN_CLOSED:
                    window.close()
                    break

                case '-ADD-':
                    if values['-USERNAME-'] and values['-PASSWORD-']:
                        create_config(values['-USERNAME-'],
                                      values['-PASSWORD-'])
                        window.close()
                        main_window()

                case '-START-':
                    timer.interval = values['-TIMER-'] * 60
                    tweet.msg = get_random_tweet(tweets)[1]
                    make_tweet(tweet, config, timer)

                case '-STOP-':
                    timer.stop()

                case '-EDIT-':
                    window.close()
                    os.remove(get_config_path())
                    main_window()

                case '-ADD_TWEET-':
                    window.close()
                    add_tweet_window(config['user'])
                    main_window()


def start():
    main_window()
