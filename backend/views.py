""" Define the views """

# pylint: disable=C0103,C0111,C0413,C0412,C0411,C0330

import os
import simplejson
from backend import app
from flask import render_template, jsonify
from helpers import get_name_from_url


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/songlist')
def songlist():
    # Current directory is the root directory
    song_data_paths = os.listdir('./backend/song_json')

    all_song_data = []

    # Open each file and read the song name
    for path in song_data_paths:
        with open('./backend/song_json/'+path, 'r') as song_file:
            text = song_file.read()
            song_data = simplejson.loads(text)

            all_song_data.append({
                'name': song_data['name'],
                'url': path.replace('.json', '')
            })

    all_song_data.sort(key=lambda s: s['name'])

    return jsonify(all_song_data)


@app.route('/song/<url>')
def song(url):
    path = './backend/song_json/{0}.json'.format(url)
    if not os.path.isfile(path):
        return jsonify({'error': 'Song not found.'})

    # Read song lyrics
    song = {}
    with open(path, 'r') as song_file:
        text = song_file.read()
        song_data = simplejson.loads(text)

        song['name'] = song_data['name']
        song['lyrics'] = song_data['lyrics']

    return jsonify(song)


@app.route('/<path:path>')
def fallback(path):
    return render_template('index.html')
