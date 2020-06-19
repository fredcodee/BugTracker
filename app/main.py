from flask import Blueprint, redirect, render_template, request, flash, url_for, abort
from app.models import User, Project
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

#user profile
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
    items_num = 10
    users = User.query.paginate(1, items_num, False).items
    pn=len(users)
    return(render_template("mra.html", users=users, pn = pn))
  else:
    abort(404)

#pagination for manage roles
@main.route("/managerole/show", methods=["GET", "POST"])
@login_required
def pagenum():
  num= request.form.get("pagenum")
  if num:
    items_num = int(num)
    users = User.query.paginate(1, items_num, False).items
    return(render_template("mra.html", users=users))
  else:
    return(redirect(url_for("main.mra")))

#search for users in manage role assignment
@main.route("/managerole/search", methods=["GET", "POST"])
@login_required
def searchuser():
  search = request.form.get("search").title()
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


#MANAGE PROJECT USERS
#view porjects
@main.route("/manageprojects")
@login_required
def manageprojects():
  projects = Project.query.all()
  return(render_template("mpr.html", projects=projects))

#view selected project
@main.route("/AddToProject/<idd>")
@login_required
def AddToProject(idd):
  if current_user.role == "Admin":
    project = Project.query.get(int(idd))
    assigned_users = project.team
    return(render_template("assign.html", project = project, assigned = assigned_users))
  else:
    abort(404)

#search user
@main.route("/AddToProject/<idd>/search", methods=["GET", "POST"])
@login_required
def searchuser2(idd):
  project = Project.query.get(int(idd))
  search = request.form.get("search").title()
  if search:
    from sqlalchemy import or_
    get_user = User.query.filter(
        or_(User.name == search, User.email == search, User.role == search)).all()
    if get_user:
      return(render_template("assign2.html", users=get_user, project = project))
    else:
      flash("user not found")
      return(redirect(url_for("main.AddToProject", idd=idd)))
  else:
    flash("please recheck and type the correct details needed")
    return(redirect(url_for("main.AddToProject", idd = idd)))

#add user to a project
@main.route("/adduser/<idd>", methods=["POST"])
@login_required
def adduser(idd):
  users = request.form.getlist('user')
  get_project = Project.query.get(int(idd))

  for user in users:
    if user in get_project.team:
      users.remove(user)
    else:
      get_user = User.query.get(int(user))
      get_project.team.append(get_user)
      db.session.commit()

  flash("changes saved")
  return(redirect(url_for("main.AddToProject", idd = idd)))

#remove users
@main.route("/remove/<idd>" , methods= ["POST", "GET"])
@login_required
def remove(idd):
  if current_user.role == 'Admin':
    if request.method == 'POST':
      users = request.form.getlist('user')
      get_project = Project.query.get(int(idd))
      for user in users:
        get_user = User.query.get(int(user))
        get_project.team.remove(get_user)
        db.session.commit()
        flash("changes saved")
        return(redirect(url_for("main.remove", idd = idd)))

    project = Project.query.get(int(idd))
    assigned_users = project.team
    return(render_template("remove.html", project=project, assigned=assigned_users))
  else:
    abort(404)

#PROJECTS
#create project
@main.route("/createproject", methods=["GET", "POST"])
@login_required
def createproject():
  if request.method == 'POST':
    project_name= request.form.get('name')
    project_description = request.form.get('description')

    project = Project(project_name=project_name, description= project_description)
    db.session.add(project)
    db.session.commit()
    flash('project created')
    return(redirect(url_for('main.createproject')))

  return(render_template('createproject.html'))

#view project
@main.route("/projects")
@login_required
def projects():
  projects = Project.query.all()
  return(render_template("projects.html", projects = projects))

#edit project
@main.route("/editproject/<idd>", methods=['POST', 'GET'])
@login_required
def edit_project(idd):
  if current_user.role == "Admin":
    project = Project.query.get(int(idd))

    if request.method == 'POST':
      project_name = request.form.get('name')
      project_description = request.form.get('description')

      project.project_name =project_name
      project.description  = project_description
      db.session.commit()
      flash('changes saved')
      return(redirect(url_for('main.projects')))

    return(render_template('editproject.html', project_id =project.id))
  else:
    abort(404)

