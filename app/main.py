from flask import Blueprint, redirect, render_template, request, flash, url_for, abort
from app.models import User
from app import db
from flask_wtf import FlaskForm
from flask_login import login_required , current_user
#from flask_wtf.file import FileField, FileAllowed
#from flask_uploads import IMAGES
#import random

main = Blueprint('main', __name__)


@main.route("/")
def index():
  return(render_template("layout.html"))

@main.route("/home")
@login_required
def home():
  return(render_template("home.html"))

@main.route("/<user>")
@login_required
def profile(user):
  if current_user.name == user:
    get_user = User.query.filter_by(name=user).first()
    return(render_template("profile.html", get_user=get_user))

#manage role assignment
@main.route("/managerole", methods=["GET","POST"])
@login_required
def mra():
  if current_user.role == "Admin":
    users=User.query.all()
    if request.method == 'POST':
      pass
  
    return(render_template("mra.html", users=users))
  else:
    abort(404)