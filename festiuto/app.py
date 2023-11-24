"""
FestiIUTo
"""

from flask_login import LoginManager
from flask import Flask
from flask_htmx import HTMX

app = Flask(__name__)
htmx = HTMX(app)

