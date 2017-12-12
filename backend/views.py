""" Define the views """

# pylint: disable=C0103,C0111,C0413,C0412,C0411,C0330

from backend import app
from flask import render_template, jsonify


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/songlist')
def songlist():
    return jsonify([
        {
            "name": "Sleigh Ride",
            "url": "sleigh-ride"
        },
        {
            "name": "White Christmas",
            "url": "white-christmas"
        }
    ])


@app.route('/<path:path>')
def fallback(path):
    return render_template('index.html')
