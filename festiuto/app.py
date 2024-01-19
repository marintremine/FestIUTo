"""
FestiIUTo
"""


from flask_login import LoginManager, current_user
from flask import Flask, flash, redirect, url_for
from flask_htmx import HTMX
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

import locale




app = Flask(__name__)
htmx = HTMX(app)

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://tremine:tremine@servinfo-maria:3306/DBtremine'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:root@localhost:3306/festiuto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root@localhost:3306/festiuto'
app.config['SECRET_KEY'] = 'iMQWPgaEP2WQQUxPvKiYiZoP5jaP5RdzGoE4msqtGFTJgSVKTwVH3SEUGsjRRTkFZMKqXKmCsAaEWbdjWJEb8ip2rNi4hCKezTxe5VVXfiAgDfYzdLRAEqf3dou8gGwr'


db: SQLAlchemy = SQLAlchemy(app)
csrf = CSRFProtect(app)
csrf.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'connexion'


def admin():
    """
    Initialisation de l'interface d'administration
    """
    class myModelView(ModelView):
        # column_display_pk = True 
        # column_hide_backrefs = False
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

   

    # app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
    #
    admin = Admin(app, name='Tableau de bord',index_view=myAdminIndexView(), template_mode='bootstrap3')

    from .models import Visiteur, Artiste, Groupe, TypeBillet, Billet, Favoris, Hebergement, Heberge, Instrument, LienRS, Lieu, Photo, ReseauSocial, Jouer, Style, SInscrit, Posseder, Video, Evenement

    class VisiteurView(myModelView):
        column_exclude_list = ['password', 'motdepasse' ]

    class artisteView(myModelView):
        column_list = ('nomA','prenomA','dateNaissA','groupe')
        form_columns = ('nomA','prenomA','dateNaissA','groupe')

    class GroupeView(myModelView):
        column_list = ('nomG','descriptionG')
        form_columns = ('nomG','descriptionG')

    class TypeBilletView(myModelView):
        column_list = ('nomB','prix','duree')
        form_columns = ('nomB','prix','duree')

    class HebergementView(myModelView):
        column_list = ('nomHebergement','addresse','nbPlaces')
        form_columns = ('nomHebergement','addresse','nbPlaces')

    class InstrumentView(myModelView):
        column_list = ('nomI',)
        form_columns = ('nomI',)

    class LieuView(myModelView):
        column_list = ('nomLieu','nbPlaces')
        form_columns = ('nomLieu','nbPlaces')

    class reseauSocialView(myModelView):
        column_list = ('nomReseau','urlLogoReseau')
        form_columns = ('nomReseau','urlLogoReseau')

    class styleView(myModelView):
        column_list = ('nomS','style')
        form_columns = ('nomS','style')

    class FavorisView(myModelView):
        column_list = ('groupe', 'visiteur') 

        form_columns = ('groupe', 'visiteur')

        form_args = {
            'groupe': {
                'query_factory': lambda: Groupe.query.all(),
                'allow_blank': False
            },
            'visiteur': {
                'query_factory': lambda: Visiteur.query.all(),
                'allow_blank': False
            }
        }
        def on_model_change(self, form, Favoris, is_created):
            db.session.commit()
            db.session.flush()


    admin.add_view(VisiteurView(Visiteur, db.session))
    admin.add_view(artisteView(Artiste, db.session))
    admin.add_view(GroupeView(Groupe, db.session))
    admin.add_view(TypeBilletView(TypeBillet, db.session))
    admin.add_view(myModelView(Billet, db.session))
    admin.add_view(FavorisView(Favoris, db.session))
    admin.add_view(HebergementView(Hebergement, db.session))
    admin.add_view(myModelView(Heberge, db.session))
    admin.add_view(InstrumentView(Instrument, db.session))
    admin.add_view(myModelView(LienRS, db.session))
    admin.add_view(LieuView(Lieu, db.session))
    admin.add_view(myModelView(Photo, db.session))
    admin.add_view(reseauSocialView(ReseauSocial, db.session))
    admin.add_view(myModelView(Jouer, db.session))
    admin.add_view(styleView(Style, db.session))
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
    flash("Vous devez être connecté pour accéder à cette page")
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

if __name__ == "__main__":
    app.run(host="127.0.0.9", port=8080, debug=True)