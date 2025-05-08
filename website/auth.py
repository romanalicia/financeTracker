from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user 
from werkzeug.security import generate_password_hash, check_password_hash

from . import db 

from .models import User 

auth = Blueprint("auth", __name__)


@auth.route("/sign-up", methods=['GET','POST'])
def sign_up(): 
    
    return render_template("sign_up.html")

@auth.route("/login")
def login(): 
    return render_template("login.html")

@auth.route("/logout")
def logout(): 
    return render_template("logout.html")