"""
FestiIUTo
"""

from flask_login import LoginManager
from flask import Flask, redirect
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect





app = Flask(__name__)
htmx = HTMX(app)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://tremine:tremine@servinfo-maria:3306/DBtremine'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:root@localhost:3306/festiuto'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root@localhost:3306/festiuto'
app.config['SECRET_KEY'] = 'iMQWPgaEP2WQQUxPvKiYiZoP5jaP5RdzGoE4msqtGFTJgSVKTwVH3SEUGsjRRTkFZMKqXKmCsAaEWbdjWJEb8ip2rNi4hCKezTxe5VVXfiAgDfYzdLRAEqf3dou8gGwr'



db: SQLAlchemy = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized_callback():
    """
    Redirection vers la page de connexion si l'utilisateur n'est pas connecté
    """
    return redirect('/connexion')


@app.cli.command('dropdb')
def dropdb_command():
    """Drops the database tables."""
    db.drop_all()
    print('Dropped the database.')


@app.cli.command('initmdp')
def initmdp_command():
    from .models import Visiteur
    print(Visiteur.generate_hash("administrateur"))


@app.cli.command("initdb")
def initdb_command():
    """Creates the database tables."""
    db.create_all()
    print("Initialized the database.")