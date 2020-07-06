from flask import Blueprint, redirect, render_template, request, flash, url_for, abort
from app.models import User, Project, Ticket, Comment, Ticket_history
from app import db
from flask_wtf import FlaskForm
from flask_login import login_required , current_user
#from flask_wtf.file import FileField, FileAllowed
#from flask_uploads import IMAGES
import random
from sqlalchemy import or_

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
  init_search = request.form.get("search")
  search = init_search.title()

  if init_search:
    get_user = User.query.filter(
        or_(User.name == search, User.email == init_search, User.role == search)).all()
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
    flash("New role assigned")
    return(redirect(url_for("main.mra")))
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
  init_search = request.form.get("search")
  search = init_search.title()

  if init_search:
    get_user = User.query.filter(
        or_(User.name == search,User.email == init_search,User.role == search)).all()
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
    project_name= request.form.get('name').title()
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

#search project
@main.route("/project/search", methods=["GET", "POST"])
def p_search():
  keyword = request.form.get('search').title()
  results = Project.query.filter_by(project_name=keyword).all()
  if results:
    return(render_template("projects.html", projects = results))
  else:
    flash("Project not found")
    return(redirect(url_for("main.projects")))

#edit project
@main.route("/editproject/<idd>", methods=['POST', 'GET'])
@login_required
def edit_project(idd):
  if current_user.role == "Admin":
    project = Project.query.get(int(idd))

    if request.method == 'POST':
      project_name = request.form.get('name').title()
      project_description = request.form.get('description')

      project.project_name =project_name
      project.description  = project_description
      db.session.commit()
      flash('changes saved')
      return(redirect(url_for('main.projects')))

    return(render_template('editproject.html', project =project))
  else:
    abort(404)

#project details
@main.route("/details/<idd>")
@login_required
def project_details(idd):
  project = Project.query.get(int(idd))

  return(render_template("projectdetails.html", project = project))

#view project tickets
@main.route("/details/tickets/<idd>")
@login_required
def project_tickets(idd):
  project = Project.query.get(int(idd))
  mytickets = Ticket.query.filter(Ticket.project_ticket.has(id=int(idd)))
  return(render_template("tickets.html", tickets=mytickets))



#TICKETS
#view tickets
@main.route("/mytickets")
@login_required
def mytickets():
  tickets = Ticket.query.all()
  #admin sees all tickets
  if current_user.role == "Admin":
    return(render_template("tickets.html", tickets=tickets))
  
  elif current_user =="Project manager":
    #project manager restricted to only theirs
    mytickets=Ticket.query.filter(Ticket.user_ticket.has(email=current_user.email))
    return(render_template("tickets.html", tickets=mytickets))
    
  elif current_user == "Developer":
    # tickets assigned to developer
    mytickets = Ticket.query.filter(assigned_dev= current_user.email)
    return(render_template("tickets.html", tickets=mytickets))
  else:
    abort(404)

#create tickets
@main.route("/mytickets/projects")
@login_required
def createticket():
  projects = Project.query.all()
  return(render_template("createticketsub.html", projects = projects))

#ticket form
@main.route("/tickets/create/<idd>", methods = ["POST", "GET"])
@login_required
def createticket_form(idd):
  project = Project.query.get(int(idd))

  #only admin and pm allowed
  if current_user.role != "Developer":
    if request.method == "POST":
      title=request.form.get("title")
      description = request.form.get("description")
      assigned = request.form.get("assigned")
      priority = request.form.get("priority")
      status = request.form.get("status")
      ticket_type = request.form.get("type")
      comment = request.form.get("comments")

      #create ref num
      ref_n = []
      for i in range(6):
        n = random.randint(0, 9)
        ref_n.append(str(n))
      ref_num = "".join(ref_n)
      
      #check assigned developer
      check_assigned_dev = User.query.filter_by(email=assigned).first()
      if check_assigned_dev:
        #save ticket to database
        new_ticket = Ticket(title = title, description = description,assigned_dev = assigned,ticket_type = ticket_type, priority = priority,status = status, ref_num = int(ref_num), user_ticket= current_user, project_ticket = project)

        db.session.add(new_ticket)
        db.session.commit()

        if comment:
          get_ticket=Ticket.query.filter_by(ref_num = int(ref_num)).first()
          new_comment = Comment(details=comment, user_comment=current_user, ticket_comments = get_ticket)
          db.session.add(new_comment)
          db.session.commit()

        flash("Ticket Created")
        return(redirect(url_for("main.mytickets")))
      else:
        flash("Assigned developer not found")
        return(redirect(url_for("main.createticket_form", idd = idd)))

    users = User.query.filter(or_(User.role == "Developer", User.role == "Project Manager")).all()
    return(render_template("createticket.html", project= project, users=users))
  else:
    abort(404)

#search and filter tickets
@main.route("/tickets/search", methods=["POST", "GET"])
@login_required
def tickets_search():
  search = request.form.get("search")
  status = request.form.get("status")

  if search:
    try:
      search = Ticket.query.filter_by(ref_num = int(search)).all()
      return(render_template("tickets.html", tickets=search))
    except:
      search = Ticket.query.filter_by(title=search).all()
      return(render_template("tickets.html", tickets=search))
  elif status:
    search = Ticket.query.filter_by(status=status).all()
    return(render_template("tickets.html", tickets=search))
  else:
    flash("ticket not found")
    return(redirect(url_for("main.mytickets")))


@main.route("/tickets/priority", methods=["POST", "GET"])
@login_required
def tickets_priority():
  priority = request.form.get("priority")
  search = Ticket.query.filter_by(priority=priority).all()
  return(render_template("tickets.html", tickets=search))

#view ticket page
@main.route("/tickets/view/<idd>")
@login_required
def view_ticket(idd):
  ticket = Ticket.query.get(int(idd))
  comments = Comment.query.filter(Comment.ticket_comments.has(id=int(idd)))
  return(render_template("ticketpage.html", ticket = ticket, comments = comments))







#written by Wilfred 
