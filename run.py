""" Run the app in debug mode """

# pylint: disable=C0103,C0111,C0413,C0412,C0411,C0330

from flask import Flask, render_template
from backend import app

app.run(debug=True)
