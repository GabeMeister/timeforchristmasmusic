""" Define the views """

# pylint: disable=C0103,C0111,C0413,C0412,C0411,C0330

import os
from backend import app
from flask import render_template, jsonify
from helpers import get_name_from_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/songlist')
def songlist():
    # Current directory is the root directory
    all_songs = os.listdir('./backend/songs')
    all_songs = map(lambda song: song.replace('.txt', ''), all_songs)
    all_songs = map(lambda song: {'name': get_name_from_url(song), 'url': song}, all_songs)

    return jsonify(all_songs)


@app.route('/song/<url>')
def song(url):
    return jsonify({
        "name": "White Christmas",
        "lyrics": "I'm dreaming of a white christmas"
    })


@app.route('/<path:path>')
def fallback(path):
    return render_template('index.html')
