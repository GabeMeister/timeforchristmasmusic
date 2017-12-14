""" flask scripts """

# pylint: disable=C0103,C0111,E1101,W0401,C0301

import os
from flask_script import Manager
from backend import app
from backend.views import songlist

manager = Manager(app)


@manager.command
def rename():
    for filename in os.listdir('./backend/songs'):
        if(' ' in filename):
            new_filename = filename.replace(' ', '-').replace("'", '').lower()
            print new_filename
            os.rename('./backend/songs/'+filename, './backend/songs/'+new_filename)

    print 'done.'


@manager.command
def get_song_list():
    ret = songlist()
    print 'ret: ' + str(ret)


if __name__ == "__main__":
    manager.run()
