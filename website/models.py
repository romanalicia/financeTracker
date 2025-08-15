"""This file defines database models including User, Goals, and Expense."""
from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


class User(db.Model, UserMixin):
    """Database model for users."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    goals = db.relationship('Goals', backref='user', passive_deletes=True)


class Goals(db.Model, UserMixin):
    """Database model for goals/savings."""

    id = db.Column(db.Integer, primary_key=True)
    # nullable=False means it can't be empty
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    goal_date = db.Column(db.Date, nullable=True)
    description = db.Column(db.Text)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)


class Expense(db.Model):
    """Database model for expenses."""

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
