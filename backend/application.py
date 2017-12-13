""" Create the app """

# pylint: disable=C0103,C0111

from flask import Flask
from flask_cors import CORS

def create_app():
    app_instance = Flask(__name__, \
        static_url_path='/static', \
        static_folder='../frontend/dist/static', \
        template_folder='../frontend/dist')
    CORS(app_instance)

    return app_instance
