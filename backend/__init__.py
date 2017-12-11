""" Initialize the package """

# pylint: disable=C0103,C0111,C0413,C0412,C0411

# The application
from backend.application import create_app
app = create_app()

# The views
from backend import views
