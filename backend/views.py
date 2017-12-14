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
    response = {'data': [], 'error': ''}

    path = './backend/songs/{0}.txt'.format(url)
    if not os.path.isfile(path):
        response['error'] = 'Song not found.'
        return jsonify(response)

    # Read song lyrics
    lyrics = ''
    with open(path, 'r') as song_file:
        lyrics = song_file.read().split('\r\n')

    return jsonify({
        "name": get_name_from_url(url),
        "lyrics": lyrics
    })


@app.route('/<path:path>')
def fallback(path):
    return render_template('index.html')
