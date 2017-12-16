""" flask scripts """

# pylint: disable=C0103,C0111,E1101,W0401,C0301

import os
import simplejson
from flask_script import Manager
from backend import app
from backend.views import songlist
from backend.helpers import get_name_from_url

manager = Manager(app)


@manager.command
def sandbox():
    path = './backend/songs/'+os.listdir('./backend/songs')[0]
    lyrics = ''
    with open(path, 'r') as song_file:
        lyrics = song_file.read().split('\r\n')

    song_data = {"lyrics": lyrics}
    song_json = simplejson.dumps(song_data, indent=4)

    with open('./backend/songs/temp.json', 'w') as song_file:
        song_file.write(song_json)

    with open('./backend/songs/temp.json', 'r') as song_file:
        text = song_file.read()
        read_song_data = simplejson.loads(text)




@manager.command
def generate_all_songs():
    all_songs = os.listdir('./backend/songs')

    for song in all_songs:
        generate_song_json(song.replace('.txt', ''))


@manager.command
def generate_song_json(file_name):
    full_file_name = file_name+'.txt'
    file_path = './backend/songs/'+full_file_name
    if not os.path.isfile(file_path):
        print 'Could not find file at: '+file_path
        return

    lyrics = ''
    with open(file_path, 'r') as song_file:
        lyrics = song_file.read().split('\r\n')

    song_data = {
        "name": get_name_from_url(file_name),
        "lyrics": lyrics
    }

    json_path = file_name+'.json'
    with open('./backend/song_json/'+json_path, 'w') as song_file:
        song_file.write(simplejson.dumps(song_data, indent=4))

    print 'Generated '+json_path


if __name__ == "__main__":
    manager.run()
