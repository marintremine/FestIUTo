from flask import render_template
from .app import app, db, htmx, csrf
from .forms import LoginForm, RegistrationForm, UpdateForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, login_required, logout_user
from jinja2_fragments.flask import render_block



from .models import Visiteur


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
    return render_template('groupe.html',title='Groupe')

@app.route('/contact')
def contact():
    return render_template('contact.html',title='Contact')

@app.route('/connexion',methods=["POST","GET"])
def connexion():
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        visiteur = Visiteur.query.filter_by(email=form.email.data).first()
        print(form.password.data)
        print(visiteur.motdepasse)
        if visiteur and Visiteur.verify_password(form.password.data, visiteur.motdepasse):
            login_user(visiteur, remember=form.remember_me.data)
            return redirect(url_for("index"))
    return render_template('login.html',title='Connexion',form=form)


@app.route('/inscription', methods=["POST","GET"])
def inscription():
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
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
        flash("You have successfully registered! You may now login.")
        return redirect(url_for("connexion"))
    return render_template('register.html',title='Inscription',form=form)


@app.route("/profil", methods=["POST","GET","PUT"])
@login_required
def profil():
    
    if htmx:
        if request.method == "POST":
            print(request.form)
        return render_block("profil.html", "details", edit=False)
    return render_template("profil.html", title="Profil", edit=False,)


@app.route("/profil/edit", methods=["POST","GET"])
def profil_edit():
    form = UpdateForm(request.form)
    return render_block("profil.html", "edit", edit=True, form=form)



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))