from flask import make_response, render_template
from .app import app, db, htmx, csrf
from .forms import LoginForm, RegistrationForm, UpdateForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from jinja2_fragments.flask import render_block
from datetime import timedelta


from .models import Artiste, Billet, Evenement, Favoris, Groupe, Instrument, Jouer, LienRS, Lieu, Photo, Posseder, ReseauSocial, SInscrit, Style, TypeBillet, Video, Visiteur


@app.route('/')
def index():
    evenements = db.session.query(Evenement).all()
    jours = []
    for evenement in evenements:
        if evenement.dateDebut.date() not in jours:
            jours.append(evenement.dateDebut.date())
    groupes = db.session.query(Groupe).all()


    favoris = db.session.query(Favoris).all()
    if current_user.is_authenticated:
        favoris = db.session.query(Favoris).filter(Favoris.idV == current_user.idV).all()


    posseder = db.session.query(Posseder).all()
    styles = db.session.query(Style).all()

    evenements = db.session.query(Evenement).all()
    photos = db.session.query(Photo).all()
    groupes_propositions = set()

    for groupe in groupes:
        for favori in favoris:
            if groupe.idG == favori.idG:
                for poss in posseder:
                    if groupe.idG == poss.idG:
                        print("Style des groupes pref :", poss.idS)
                        for groupe2 in groupes:
                            for poss2 in posseder:
                                if groupe2.idG == poss2.idG:
                                    if poss.idS == poss2.idS:
                                        groupes_propositions.add(groupe2)

    return render_template('index.html',title='FestiIUTo',groupes=groupes,jours=jours, favoris=favoris,styles=styles, groupes_propositions=groupes_propositions, evenements=evenements,photos=photos)


@app.route('/billetterie')
def billetterie():
    evenements = db.session.query(Evenement).all()
    debut = min(evenement.dateDebut.date() for evenement in evenements)
    fin = max(evenement.dateFin.date() for evenement in evenements)
    
    type_billets = db.session.query(TypeBillet).all()
    print(debut,fin)
    return render_template('billetterie.html',title='Billetterie',type_billets=type_billets,debut=debut,fin=fin)


@app.route('/billets')
@login_required
def billets():
    type_billets = db.session.query(TypeBillet).all()
    billets = db.session.query(Billet).filter(Billet.idV == current_user.idV).all()
    reservations = db.session.query(SInscrit).filter(SInscrit.idV == current_user.idV).all()
    evenements = db.session.query(Evenement).all()
    lieux = db.session.query(Lieu).all()
    return render_template('billets.html',title='Billets',type_billets=type_billets,billets=billets,reservations=reservations,evenements=evenements, lieux=lieux)


@app.route('/billetterie/achat', methods=["GET"])
@login_required
def achat():
    billet = Billet(idV=current_user.idV, idTb=request.args.get("idTb"), dateDebutValidite=request.args.get("dateDebutValidite"))
    if billet == None:
        flash("Erreur lors de l'achat du billet.",'error')
        return redirect(url_for("billetterie"))
    
    if db.session.query(Billet).filter(Billet.idV == current_user.idV, Billet.idTb == billet.idTb, Billet.dateDebutValidite == billet.dateDebutValidite ).count() > 0:
        flash("Vous avez déjà un billet de ce type.",'error')
        return redirect(url_for("billetterie"))

    db.session.add(billet)
    db.session.commit()
    flash("Billet acheté avec succès.",'success')
    return redirect(url_for("billets"))


@app.route('/participe/')
@login_required
def participe():
    if not current_user.is_authenticated:
        flash("Vous devez être connecté pour participer à l'événement.",'error')
        return redirect(url_for("connexion"))
    s_inscrit = SInscrit(idEv=request.args.get("idEv"), idV=current_user.idV)


    evenement = db.session.query(Evenement).filter(Evenement.idEv == request.args.get("idEv")).first()
    lieu = db.session.query(Lieu).filter(Lieu.idL == evenement.idL).first()
    

    if db.session.query(SInscrit).filter(SInscrit.idEv == request.args.get("idEv"), SInscrit.idV == current_user.idV).first():
        flash("Vous participez déjà à l'événement.",'error')
        return redirect(url_for("billets"))

    if db.session.query(SInscrit).filter(SInscrit.idEv == request.args.get("idEv")).count() >= lieu.nbPlaces:
        flash("L'événement est complet.",'error')
        return redirect(url_for("programmation"))

    if evenement.gratuit:
        db.session.add(s_inscrit)
        db.session.commit()
        flash("Vous participez à l'événement avec succès.",'success')
        return redirect(url_for("billets"))


    if db.session.query(Billet).filter(Billet.idV == current_user.idV).count() == 0:
        flash("Vous devez avoir un billet pour participer à l'événement.",'error')
        return redirect(url_for("billetterie"))


    for billet in db.session.query(Billet).filter(Billet.idV == current_user.idV).all():
        type_billet = db.session.query(TypeBillet).filter(TypeBillet.idTb == billet.idTb).first()


        if type_billet.duree == None or (billet.dateDebutValidite <= evenement.dateDebut.date() and billet.dateDebutValidite + timedelta(days=type_billet.duree) >= evenement.dateFin.date()) :
            db.session.add(s_inscrit)
            db.session.commit()
            flash("Vous participez à l'événement avec succès.",'success')
            return redirect(url_for("billets"))
    
    flash("Vous devez avoir un billet valide pour participer à l'événement.",'error')
    return redirect(url_for("billetterie"))


@app.route('/desinscription/')
@login_required
def desinscription():
    if not current_user.is_authenticated:
        flash("Vous devez être connecté pour vous désinscrire de l'événement.",'error')
        return redirect(url_for("connexion"))
    s_inscrit = db.session.query(SInscrit).filter(SInscrit.idEv == request.args.get("idEv"), SInscrit.idV == current_user.idV).first()
    if s_inscrit == None:
        flash("Vous ne participez pas à l'événement.",'error')
        return redirect(url_for("billets"))
    db.session.delete(s_inscrit)
    db.session.commit()
    flash("Vous vous êtes désinscrit de l'événement avec succès.",'success')
    return redirect(url_for("billets"))

@app.route('/programmation')
def programmation():
    evenements = db.session.query(Evenement).all()
    lieux = db.session.query(Lieu).all()
    jours = []
    reservations = []
    for evenement in evenements:
        reservations.append({"idEv":evenement.idEv, "nb":db.session.query(SInscrit).filter(SInscrit.idEv == evenement.idEv).count()})
        if evenement.dateDebut.date() not in jours:
            jours.append(evenement.dateDebut.date())
    

    photos = db.session.query(Photo).all()
    

    return render_template('programmation.html',title='Programmation',evenements=evenements,jours=jours, lieux=lieux,photos=photos,reservations=reservations)

@app.route('/groupe')
def groupe():
    groupes = db.session.query(Groupe)
    posseder = db.session.query(Posseder).all()
    styles = db.session.query(Style).all()
    artistes = db.session.query(Artiste).all()
    lien_rs = db.session.query(LienRS).all()
    reseau_social = db.session.query(ReseauSocial).all()
    photos = db.session.query(Photo).all()
    suggestions = []
    favoris = db.session.query(Favoris).all()

    if current_user.is_authenticated:
        favoris = db.session.query(Favoris).filter(Favoris.idV == current_user.idV).all()
        print(favoris)
    if htmx:
        q = request.args.get('q')
        style = request.args.get('style')
        if q:
            groupes = groupes.filter(Groupe.nomG.like("%"+q+"%"))
        if style and style != "all" and style != "fav":
            groupes = groupes.join(Posseder).join(Style).filter(Style.nomS.like("%"+style+"%"))
            suggestions = db.session.query(Style).filter(Style.idS_2 == db.session.query(Style).filter(Style.nomS == style).first().idS_1).all()
            print(suggestions)
        if style == "fav":
            groupes = groupes.join(Favoris).filter(Favoris.idV == current_user.idV)
        groupes = groupes.all()
        return render_block("groupe.html", "results", groupes=groupes,styles=styles,artistes=artistes,posseder=posseder,lien_rs=lien_rs,reseau_social=reseau_social,photos=photos,favoris=favoris,suggestions=suggestions)

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

@app.route('/fav/<int:id>')
@login_required
def fav(id):
    favoris = Favoris(idV=current_user.idV, idG=id)
    db.session.add(favoris)
    db.session.commit()
    return render_block("groupe.html", "fav", id=id)


@app.route('/unfav/<int:id>')
@login_required
def unfav(id):
    favoris = db.session.query(Favoris).filter(Favoris.idV == current_user.idV, Favoris.idG == id).first()
    db.session.delete(favoris)
    db.session.commit()
    return render_block("groupe.html", "unfav", id=id)

@app.route('/details/<int:id>')
def details(id):
    groupe = db.session.query(Groupe).get(id)
    artistes = db.session.query(Artiste).all()
    videos = db.session.query(Video).all()
    instruments = db.session.query(Instrument).all()
    jouer = db.session.query(Jouer).all()
    return render_template('details.html',title='Details', groupe=groupe,artistes=artistes,videos=videos,instruments=instruments,jouer=jouer)


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



# @LoginManager.unauthorized_handler
# def unauthorized():
#     return redirect(url_for('connexion'))

# @app.route("/admin")
# @login_required
# def admin():
#     if current_user.admin:
#         return render_template("admin.html", title="Admin")
#     else:
#         return redirect(url_for("index"))