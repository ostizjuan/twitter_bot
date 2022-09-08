import os
import sqlite3


def create_table():
    if not os.path.isfile('tweets.db'):
        conn = sqlite3.connect('tweets.db')
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS tweets(id INTEGER PRIMARY KEY AUTOINCREMENT, msg TEXT, user TEXT)')
        conn.commit()
        conn.close()


def add_tweet(msg, user):
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tweets (msg, user) VALUES (?, ?)', (msg, user))
    conn.commit()
    conn.close()


def get_tweets(user):
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tweets WHERE user = ?', (user,))
    tweets = cursor.fetchall()
    conn.close()
    return tweets


def delete_tweet(id, user):
    conn = sqlite3.connect('tweets.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tweets WHERE id = ? AND user = ?', (id, user))
    conn.commit()
    conn.close()
