from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from .models import Goals
from .models import Expense
from . import db
from datetime import datetime

views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)


@views.route("/track-expenses", methods=['GET', 'POST'])
@login_required
def track_expenses():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        description = request.form.get('content')  # optional

        # Validation
        if not category or not amount:
            flash('Category and amount are required.', 'error')
            return redirect(url_for('views.track_expenses'))

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            flash('Please enter a valid amount greater than 0.', 'error')
            return redirect(url_for('views.track_expenses'))

        # Save to DB
        new_expense = Expense(
            category=category,
            amount=amount,
            description=description,
            user_id=current_user.id
        )
        db.session.add(new_expense)
        db.session.commit()

        flash('Expense added successfully!', 'success')
        return redirect(url_for('views.track_expenses'))

    # GET request: show all user's expenses
    expenses = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date_created.desc()).all()
    return render_template("track_expenses.html", user=current_user, expenses=expenses)


@views.route("/goals-and-savings", methods=['GET', 'POST'])
@login_required
def goals_and_savings():
    if request.method == "POST":
        title = request.form.get('title')
        amount = request.form.get('amount')
        goal_date = request.form.get('goal_date')
        goal_date_str = request.form.get('goal_date')
        goal_date = datetime.strptime(goal_date_str, '%Y-%m-%d').date()
        description = request.form.get('description')

        if not title:
            flash('Title cannot be empty', category="error")
        elif not amount:
            flash('Please set an amount', category='error')
        elif not goal_date:
            flash('Please provide a goal date', category='error')
        else:
            new_goal = Goals(
                title=title,
                amount=amount,
                goal_date=goal_date,
                description=description,
                author=current_user.id
            )
            db.session.add(new_goal)
            db.session.commit()
            flash('Your goal has been added!', category='success')
        return redirect(url_for('views.goals_and_savings'))

    author_goals = Goals.query.filter_by(author=current_user.id).all()
    return render_template("goals-and-savings.html", user=current_user, goals=author_goals)
