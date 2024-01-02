"""
FestiIUTo
"""

from flask_login import LoginManager, current_user, login_required
from flask import Flask, flash, redirect, request, url_for
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView





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


def admin():
    """
    Initialisation de l'interface d'administration
    """
    class myModelView(ModelView):
        def is_accessible(self):
            return current_user.is_authenticated and current_user.admin
        def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
            flash("Vous n'avez pas accès à cette page")
            return redirect(url_for('connexion'))
        
    class myAdminIndexView(AdminIndexView):
        @expose('/')
        def index(self):
            if current_user.is_authenticated and current_user.admin:
                return self.render('admin/index.html')
            else:
                flash("Vous n'avez pas accès à cette page")
                return redirect(url_for('connexion'))
        

    from .models import Visiteur, Artiste, Groupe, TypeBillet, Billet, Favoris, Hebergement, Heberge, Instrument, LienRS, Lieu, Photo, ReseauSocial, Jouer, Style, SInscrit, Posseder, Video, Evenement
    admin = Admin(app, name='Tableau de bord',index_view=myAdminIndexView, template_mode='bootstrap3')


    admin.add_view(myModelView(Visiteur, db.session))
    admin.add_view(myModelView(Artiste, db.session))
    admin.add_view(myModelView(Groupe, db.session))
    admin.add_view(myModelView(TypeBillet, db.session))
    admin.add_view(myModelView(Billet, db.session))
    admin.add_view(myModelView(Favoris, db.session))
    admin.add_view(myModelView(Hebergement, db.session))
    admin.add_view(myModelView(Heberge, db.session))
    admin.add_view(myModelView(Instrument, db.session))
    admin.add_view(myModelView(LienRS, db.session))
    admin.add_view(myModelView(Lieu, db.session))
    admin.add_view(myModelView(Photo, db.session))
    admin.add_view(myModelView(ReseauSocial, db.session))
    admin.add_view(myModelView(Jouer, db.session))
    admin.add_view(myModelView(Style, db.session))
    admin.add_view(myModelView(SInscrit, db.session))
    admin.add_view(myModelView(Posseder, db.session))
    admin.add_view(myModelView(Video, db.session))
    admin.add_view(myModelView(Evenement, db.session))

admin()
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