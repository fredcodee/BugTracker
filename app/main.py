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

#show all users for manage role assignment
@main.route("/managerole", methods=["GET","POST"])
@login_required
def mra():
  if current_user.role == "Admin":
    users=User.query.all()
    return(render_template("mra.html", users=users))
  else:
    abort(404)

#search for user in manage role assignment
@main.route("/managerole/search", methods=["GET", "POST"])
@login_required
def searchuser():
  search = request.form.get("search")
  if search:
    from sqlalchemy import or_
    get_user= User.query.filter(or_(User.name == search, User.email == search, User.role == search)).all()
    if get_user:
      return(render_template("mra.html", users=get_user))
    else:
      flash("user not found")
      return(redirect(url_for("main.mra")))
  else:
    flash("please recheck and type the correct details needed")
    return(redirect(url_for("main.mra")))

#assign role
@main.route("/assign/<idd>", methods=["POST"])
@login_required
def assign(idd):
  get_user = User.query.get(int(idd))
  role = request.form.get("selection")

  if get_user and role != "SL":
    get_user.role = role
    db.session.commit()
    return(redirect(url_for("main.mra")))
    flash("New role assigned")
  else:
    flash("invalid / no role was assigned")
    return(redirect(url_for("main.mra")))

  
