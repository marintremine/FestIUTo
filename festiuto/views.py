from flask import render_template
from .app import app, db, htmx, csrf
from .forms import LoginForm, RegistrationForm, UpdateForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from jinja2_fragments.flask import render_block



from .models import Artiste, Favoris, Groupe, Instrument, Jouer, LienRS, Photo, Posseder, ReseauSocial, Style, Video, Visiteur


@app.route('/')
def index():
    
    return render_template('index.html',title='FestiIUTo')


@app.route('/billetterie')
def billetterie():
    return render_template('billetterie.html',title='Billetterie')

@app.route('/programmation')
def programmation():
    return render_template('programmation.html',title='Programmation')

@app.route('/groupe')
def groupe():
    groupes = db.session.query(Groupe)
    posseder = db.session.query(Posseder).all()
    styles = db.session.query(Style).all()
    artistes = db.session.query(Artiste).all()
    lien_rs = db.session.query(LienRS).all()
    reseau_social = db.session.query(ReseauSocial).all()
    photos = db.session.query(Photo).all()
    favoris = db.session.query(Favoris).all()

    if htmx:
        q = request.args.get('q')
        style = request.args.get('style')
        if q:
            groupes = groupes.filter(Groupe.nomG.like("%"+q+"%"))
        if style and style != "all":
            groupes = groupes.join(Posseder).join(Style).filter(Style.nomS.like("%"+style+"%"))
        groupes = groupes.all()
        return render_block("groupe.html", "results", groupes=groupes,styles=styles,artistes=artistes,posseder=posseder,lien_rs=lien_rs,reseau_social=reseau_social,photos=photos,favoris=favoris)

    groupes = groupes.all()
    return render_template('groupe.html',title='Groupe',groupes=groupes,styles=styles,artistes=artistes,posseder=posseder,lien_rs=lien_rs,reseau_social=reseau_social,photos=photos,favoris=favoris)

@app.route('/groupe/search', methods=["POST","GET"])
def search():
    q =  request.args.get('q')
    print(q)
    if q:
        groupes = db.session.query(Groupe).filter(Groupe.nomG.like("%"+q+"%")).all()
        return render_template('groupe.html',title='Groupe',groupes=groupes)
    return render_template('groupe.html.html',title='Groupe')

@app.route('/details/<int:id>')
def details(id):
    groupe = db.session.query(Groupe).get(id)
    artistes = db.session.query(Artiste).all()
    videos = db.session.query(Video).all()
    instruments = db.session.query(Instrument).all()
    jouer = db.session.query(Jouer).all()
    return render_template('details.html',title='Details', groupe=groupe,artistes=artistes,videos=videos,instruments=instruments,jouer=jouer)


@app.route('/contact')
def contact():
    return render_template('contact.html',title='Contact')

@app.route('/connexion',methods=["POST","GET"])
def connexion():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        visiteur = Visiteur.query.filter_by(email=form.email.data).first()
        if visiteur and Visiteur.verify_password(form.password.data, visiteur.motdepasse):
            login_user(visiteur, remember=form.remember_me.data)
            flash("Connecté avec succès.", 'success')
            return redirect(url_for("index"))
    return render_template('login.html', title='Connexion', form=form)


@app.route('/inscription', methods=["POST","GET"])
def inscription():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if Visiteur.query.filter_by(email=form.email.data).first():
            flash("Adresse e-mail déjà enregistrée !",'error')
            return redirect(url_for("inscription"))
        visiteur = Visiteur(
            nomV=form.lastname.data,
            prenomV=form.firstname.data,
            motdepasse=Visiteur.generate_hash(form.password.data),
            email=form.email.data,
            dateNaissV=form.birthdate.data,
            numtel=form.numtel.data
        )
        db.session.add(visiteur)
        db.session.commit()
        flash("Vous vous êtes inscrit avec succès ! Vous pouvez maintenant vous connecter.",'info')
        return redirect(url_for("connexion"))
    return render_template('register.html',title='Inscription',form=form)


@app.route("/profil", methods=["POST","GET","PUT"])
@login_required
def profil():
    form = UpdateForm(request.form)



    if htmx:
        if request.method == "GET":
            print('show edit')
            form.firstname.data = current_user.prenomV
            form.lastname.data = current_user.nomV
            form.email.data = current_user.email
            form.birthdate.data = current_user.dateNaissV
            form.numtel.data = current_user.numtel
            return render_block("profil.html", "edit", edit=True, form=form)
        else:
            print('annuler')
            return render_block("profil.html", "details", edit=False)
    else:
        if request.method == "POST": 
            if form.validate_on_submit():
                print('edit validate')
                current_user.nomV = request.form.get("lastname")
                current_user.prenomV = request.form.get("firstname")
                current_user.email = request.form.get("email")
                current_user.dateNaissV = request.form.get("birthdate")
                current_user.numtel = request.form.get("numtel")
                db.session.commit()
                flash("Modifications enregistrées avec succès.",'success')
                return render_template("profil.html", title="Profil", edit=False, form=form)
            else:
                flash("Erreur dans le formulaire.",'error')
                return render_template("profil.html", title="Profil", edit=True, form=form)
        else:
            return render_template("profil.html", title="Profil", edit=False, form=form)

    



    



@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.",'info')
    return redirect(url_for("index"))