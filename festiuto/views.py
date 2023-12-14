from flask import render_template
from .app import app, db
from .forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user

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
            print("Logged in successfully.")
            flash("Logged in successfully.")
            return redirect(url_for("index"))
        flash("Incorrect email or password.")
        print("Incorrect email or password.")
    return render_template('login.html',title='Connexion',form=form)


@app.route('/inscription', methods=["POST"])
def inscription():



    return render_template('register.html',title='Inscription')
