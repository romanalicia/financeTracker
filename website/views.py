from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import Goals
from . import db

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
def goals_and_savings():
    if request.method == "POST":
        title = request.form.get('title')
        amount = request.form.get('amount')
        description = request.form.get('description')
        # goal_date = request.form.get('goal_date')

        if not title:
            flash('Title cannot be empty', category="error")
        elif not amount:
            flash('Please set an amount', category='error')
        else:
            new_goal = Goals(title=title, amount=amount,
                             description=description, author=current_user.id)
            db.session.add(new_goal)
            db.session.commit()
            flash('Your goal has been added!', category='success')
        return redirect(url_for('views.goals_and_savings'))

    author_goals = Goals.query.filter_by(author=current_user.id).all()
    return render_template("goals-and-savings.html", user=current_user, goals=author_goals)
