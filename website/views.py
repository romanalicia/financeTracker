from flask import Blueprint, render_template, request, flash
from flask_login import login_user, logout_user, login_required, current_user

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/track-expenses", methods=['GET', 'POST'])
@login_required
def track_expenses():
    return render_template("track_expenses.html", user=current_user)


@views.route("/goals-and-savings", methods=['GET', 'POST'])
@login_required
def goals_and_expenses():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')

    if not title:
        flash('Title cannot be empty')

    return render_template("goals-and-savings.html", user=current_user)
