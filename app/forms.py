from flask import Blueprint, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app import db
from flask_login import login_user, login_required, logout_user

forms = Blueprint('forms', __name__)


class LoginForm(FlaskForm):
  email = StringField('email', validators=[InputRequired()])
  password = PasswordField('password', validators=[InputRequired()])
  remember = BooleanField('remember me')
  submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
  email = StringField('email', validators=[InputRequired(), Email( message='Invalid email'), Length(max=50)])
  name = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=80)])
  role = StringField('username', validators=[InputRequired()])