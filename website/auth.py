from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

from . import db 

from .models import User 

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists: 
            flash('Email is already in use.', category='error')
        elif username_exists: 
            flash('Username is already in use.', category='error')
        elif password1 != password2: 
            flash('Passwords do not match.', category='error')
        elif len(password1) < 8: 
            flash('Password is too short.', category='error')
        elif len(username) < 2: 
            flash('Username is too short.', category='error')
        elif len(email) < 4: 
            flash('Email is not valid.', category='error')
        else: 
            new_user = User(email=email, username=username, password=generate_password_hash(password1, method='scrypt:32768:8:1'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")

@auth.route("/login")
def login(): 
    return render_template("login.html")

@auth.route("/logout")
def logout(): 
    return render_template("logout.html")