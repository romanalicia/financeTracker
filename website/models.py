from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin


# database model for user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    goals = db.relationship('Goals', backref='user', passive_deletes=True)


# database model for goals/savings
class Goals(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False means it can't be empty
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # goal_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(1000))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    author = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
