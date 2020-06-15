from flask_login import UserMixin
from datetime import datetime
from app import db

assign = db.Table('assign', db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True))


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  name = db.Column(db.String(80), nullable=False)
  password = db.Column(db.String(100))
  role = db.Column(db.String(100), nullable=False)
  projects = db.relationship("Project", secondary=assign, backref='team')
  tickets = db.relationship('Ticket', backref='user_ticket', lazy='dynamic')

class Project(db.Model):
  __tablename__ = 'project'
  id = db.Column(db.Integer, primary_key=True)
  project_name = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(200))
  Project_tickets = db.relationship('Ticket', backref='project_ticket', lazy='dynamic')


class Ticket(db.Model):
  __tablename__ = 'ticket'
  id = db.Column(db.Integer, primary_key=True)
  ticket_name = db.Column(db.String(120), nullable=False)
  ticket_description = db.Column(db.String(120), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
