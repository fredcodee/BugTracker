from flask_login import UserMixin
from datetime import datetime
from app import db


class User(UserMixin, db.Model):
  __tablename__= 'users'
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  name = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(100))
  role = db.Column(db.String(100), nullable=False)
  #qoutes = db.relationship('Favourites', backref='fav', lazy=True)

class Project(db.Model):
  __tablename__ = 'projects'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(200))

class Ticket(db.Model):
   __tablename__ = 'tickets'
  pass
