"""
FestiIUTo
"""

from flask_login import LoginManager
from flask import Flask
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
htmx = HTMX(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SECRET_KEY'] = 'iMQWPgaEP2WQQUxPvKiYiZoP5jaP5RdzGoE4msqtGFTJgSVKTwVH3SEUGsjRRTkFZMKqXKmCsAaEWbdjWJEb8ip2rNi4hCKezTxe5VVXfiAgDfYzdLRAEqf3dou8gGwr'

db: SQLAlchemy = SQLAlchemy(app)


@app.cli.command("initdb")
def initdb_command():
    """Creates the database tables."""
    db.create_all()
    print("Initialized the database.")