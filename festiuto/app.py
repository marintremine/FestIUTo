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
from sqlalchemy import inspect

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
        
    # class billetView(myModelView):
    #     column_list = ('idB','dateDebutValidite', 'idV', 'idTb')
    #     form_columns = ('idB','dateDebutValidite', 'idV', 'idTb')

    # class hebergeView(myModelView):
    #     column_list = ('idG','idH', 'dateDebut', 'dateFin')
    #     form_columns = ('idG','idH', 'dateDebut', 'dateFin')

    # class lienRSView(myModelView):
    #     column_list = ('idG','idRs','pos','pseudo', 'urlReseau')
    #     form_columns = ('idG','idRs','pos','pseudo', 'urlReseau')

    # class favorisView(myModelView):
    #     column_list = ('idG','idV')
    #     form_columns = ('idG','idV')

    # class photoView(myModelView):
    #     column_list = ('idPh','idG','urlPh', 'pos')
    #     form_columns =  ('idPh','idG','urlPh', 'pos')

    # class s_inscritView(myModelView):
    #     column_list = ('idEv','idV')
    #     form_columns = ('idEv','idV')
        
    # class videoView(myModelView):
    #     column_list = ('idVideo','idG','urlVideo', 'pos')
    #     form_columns = ('idVideo','idG','urlVideo', 'pos')

    # class evenementView(myModelView):
    #     column_list = ('idEv','typeEv','descrEv','tempsMontage','tempsDemontage','gratuit','dateDebut','dateFin','idG','idL')
    #     form_columns = ('idEv','typeEv','descrEv','tempsMontage','tempsDemontage','gratuit','dateDebut','dateFin','idG','idL')

    # class artisteView(myModelView):
    #     column_list = ('nomA','prenomA','dateNaissA','idG')
    #     form_columns = ('nomA','prenomA','dateNaissA','idG')

    # class jouerView(myModelView):
    #     column_list = ('idI','idA')
    #     form_columns = ('idI','idA')

    # class possederView(myModelView):
    #     column_list = ('idG','idS')
    #     form_columns = ('idG','idS')

    # class styleView(myModelView):
    #     column_list = ('idS_1','idS_2','nomS')
    #     form_columns = ('idS_1','idS_2','nomS')

    

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
    admin.add_view(myModelView(Artiste, db.session))
    admin.add_view(myModelView(Groupe, db.session))
    admin.add_view(myModelView(TypeBillet, db.session))
    admin.add_view(myModelView(Billet, db.session))
    admin.add_view(FavorisView(Favoris, db.session))
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

if __name__ == "__main__":
    app.run(host="127.0.0.9", port=8080, debug=True)