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
  ticket_comment =db.relationship('Comment', backref='user_comment', lazy='dynamic')

class Project(db.Model):
  __tablename__ = 'project'
  id = db.Column(db.Integer, primary_key=True)
  project_name = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(200))
  Project_tickets = db.relationship('Ticket', backref='project_ticket', cascade="all,delete", lazy='dynamic')


class Ticket(db.Model):
  __tablename__ = 'ticket'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(120), nullable=False)
  description = db.Column(db.String(120), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
  status = db.Column(db.String(50), nullable=False)
  priority = db.Column(db.String(70), nullable=False)
  ticket_type = db.Column(db.String(50), nullable=False)
  ref_num = db.Column(db.Integer, nullable=False)
  date = db.Column(db.DateTime, default=datetime.utcnow)
  comments = db.relationship('Comment', backref='ticket_comments', cascade="all,delete", lazy='dynamic')
  assigned_dev = db.Column(db.String(120))#email
  history = db.relationship('Ticket_history', backref='ticket_history', cascade="all,delete", lazy='dynamic')


class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  details = db.Column(db.String(400))
  image = db.Column(db.String(500))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
  date = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket_history(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  details = db.Column(db.String(500))
  ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
  date = db.Column(db.DateTime, default=datetime.utcnow)


