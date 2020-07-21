from flask import Blueprint, redirect, render_template, request, flash, url_for, abort
from app.models import User, Project, Ticket, Comment, Ticket_history
from app.forms import Comments
from app import db, photos
from flask_login import login_required , current_user
import random
from sqlalchemy import or_ , and_

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

#show all users for manage role assignment(Admin)
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

#pagination for manage roles(Admin)
@main.route("/managerole/show", methods=["GET", "POST"])
@login_required
def pagenum():
  if current_user.role == "Admin":
    num= request.form.get("pagenum")
    if num:
      items_num = int(num)
      users = User.query.paginate(1, items_num, False).items
      return(render_template("mra.html", users=users))
    else:
      return(redirect(url_for("main.mra")))
  else:
    abort(404)

#search for users in manage role assignment(Admin)
@main.route("/managerole/search", methods=["GET", "POST"])
@login_required
def searchuser():
  if current_user.role == "Admin":
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
  else:
    abort(404)

#assign role (Admin)
@main.route("/assign/<idd>", methods=["POST"])
@login_required
def assign(idd):
  if current_user.role == "Admin":
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
  else:
    abort(404)

#delete user(Admin)
@main.route("/manageusers/delete/<idd>")
@login_required
def delete_user(idd):
  if current_user.role == "Admin":
    get_user = User.query.get(int(idd))
    if get_user:
      db.session.delete(get_user)
      db.session.commit()
      flash("user deleted")
      return(redirect(url_for("main.mra")))
  else:
    abort(404)

#MANAGE PROJECT USERS (Admin & Project Manager)
#view porjects
@main.route("/manageprojects")
@login_required
def manageprojects():
  if current_user.role == "Admin" or current_user.role == "Project Manager":
    projects = Project.query.all()
    return(render_template("mpr.html", projects=projects))
  else:
    abort(404)

#view selected project
@main.route("/AddToProject/<idd>")
@login_required
def AddToProject(idd):
  if current_user.role == "Admin" or current_user.role == "Project Manager":
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
  if current_user.role == "Admin" or current_user.role == "Project Manager":
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
#create project(Admin)
@main.route("/createproject", methods=["GET", "POST"])
@login_required
def createproject():
  if current_user.role == "Admin":
    if request.method == 'POST':
      project_name= request.form.get('name').title()
      project_description = request.form.get('description')

      project = Project(project_name=project_name, description= project_description)
      db.session.add(project)
      db.session.commit()

      get_project = Project.query.filter_by(project_name=project_name).first()
      flash('project created')
      return(redirect(url_for('main.AddToProject', idd=get_project.id)))

    return(render_template('createproject.html'))
  else:
    abort(404)

#view project
@main.route("/projects")
@login_required
def projects():
  if current_user.role == "Admin":
    projects = Project.query.all()
  elif current_user.role == "Project Manager" or current_user.role == "Developer":
    projects=Project.query.filter(Project.team.any(id = current_user.id)).all()
  return(render_template("projects.html", projects = projects))

#search project
@main.route("/project/search", methods=["GET", "POST"])
def p_search():
  keyword = request.form.get('search').title()
  results = Project.query.filter_by(project_name=keyword).all()
  user_projects = Project.query.filter(
      Project.team.any(id=current_user.id)).all()

  if results:
    if current_user.role == "Admin":
      return(render_template("projects.html", projects = results))
    elif current_user.role != "Admin":
      results=[]
      for user_project in user_projects:
        if user_project.project_name == keyword:
          results.append(user_project)
      if len(results) == 0:
        flash("Project not found")
        return(redirect(url_for("main.projects")))
      return(render_template("projects.html", projects=results))
  else:
    flash("Project not found")
    return(redirect(url_for("main.projects")))

#edit project (Admin)
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
  mytickets = Ticket.query.filter(Ticket.project_ticket.has(id=int(idd)))
  return(render_template("tickets.html", tickets=mytickets))

#delete project
@main.route("/projects/delete/<idd>")
@login_required
def delete_project(idd):
  get_project = Project.query.get(int(idd))
  db.session.delete(get_project)
  db.session.commit()
  flash("project deleted")
  return(redirect(url_for("main.projects")))


#TICKETS

#TICKET HISTORY
def add_log(name,get_ticket,log):
  #add log to ticket history
  log=Ticket_history(details="%s %s " %(name, log),ticket_history = get_ticket )
  db.session.add(log)
  db.session.commit()

#view tickets
@main.route("/mytickets")
@login_required
def mytickets():
  #admin and pm sees all tickets
  if current_user.role == "Admin" or current_user.role == "Project Manager":
    get_mytickets = Ticket.query.filter(Ticket.user_ticket.has(id=current_user.id))
    get_myassigned_tickets = Ticket.query.all()
    return(render_template("tickets.html",mytickets=get_mytickets, tickets=get_myassigned_tickets))
  
  elif current_user.role == "Developer":
    # restricted to only theirs
    mytickets = Ticket.query.filter_by(assigned_dev=current_user.email).all()
    return(render_template("tickets.html", tickets=mytickets))
  else:
    abort(404)

#create tickets(Admin & ProjectManager)
@main.route("/mytickets/projects")
@login_required
def createticket():
  if current_user.role == "Admin" or current_user.role == "Project Manager":
    projects = Project.query.all()
    return(render_template("createticketsub.html", projects = projects))
  else:
    abort(404)

#ticket form(Admin & ProjectManager)
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

        #add log to ticket history
        get_ticket = Ticket.query.filter_by(title=title).first()
        log = "created this ticket"
        add_log(current_user.name, get_ticket, log)

        flash("Ticket Created")
        return(redirect(url_for("main.mytickets")))
      else:
        flash("Assigned developer not found")
        return(redirect(url_for("main.createticket_form", idd = idd)))

    users =project.team
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
      if current_user.role == "Admin":
        search = Ticket.query.filter_by(ref_num = int(search)).all()
      elif current_user.role == "Developer" or current_user.role =="Project Manager":
        search = Ticket.query.filter(and_(Ticket.ref_num == int(search), Ticket.assigned_dev == current_user.email)).all()
      return(render_template("tickets.html", tickets=search))
    except:
      if current_user.role == "Admin":
        search = Ticket.query.filter_by(title=search).all()
      elif current_user.role == "Developer" or current_user.role == "Project Manager":
        search = Ticket.query.filter(and_(Ticket.title == search, Ticket.assigned_dev == current_user.email)).all()
      return(render_template("tickets.html", tickets=search))
  elif status:
    if current_user.role != "Admin":
      search = Ticket.query.filter(and_(Ticket.status == status, Ticket.assigned_dev == current_user.email)).all()
    else:
      search = Ticket.query.filter_by(status=status).all()
    return(render_template("tickets.html", tickets=search))
  else:
    flash("ticket not found")
    return(redirect(url_for("main.mytickets")))


@main.route("/tickets/priority", methods=["POST", "GET"])
@login_required
def tickets_priority():
  priority = request.form.get("priority")

  if current_user.role != "Admin":
    search = Ticket.query.filter(and_(Ticket.priority == priority, Ticket.assigned_dev == current_user.email)).all()
  else:
    search = Ticket.query.filter_by(priority=priority).all()
  return(render_template("tickets.html", tickets=search))

#view ticket page
@main.route("/tickets/view/<idd>", methods =["POST","GET"])
@login_required
def view_ticket(idd):
  ticket = Ticket.query.get(int(idd))

  #add comment
  form = Comments()
  if request.method == "POST" and form.validate_on_submit():
    #treating empty data werkzeug.FileStorage with try&except
    try:
      images = form.image.data
      if not images or images == " ":
        new_comment = Comment(details=form.comment.data, image=" ", user_comment=current_user, ticket_comments=ticket)
      else:
        new_comment = Comment(details=form.comment.data, image=photos.save(images), user_comment=current_user, ticket_comments= ticket)
      db.session.add(new_comment)
      db.session.commit()
      #addlog to ticket history
      log= "commented on this ticket"
      add_log(current_user.name, ticket, log)
      flash("comment added")
      return(redirect(url_for("main.view_ticket", idd=idd)))
    except:
      flash("empty field")
      return(redirect(url_for("main.view_ticket", idd=idd)))
    

  comments = Comment.query.filter(Comment.ticket_comments.has(id=int(idd)))
  history= Ticket_history.query.filter(Ticket_history.ticket_history.has(id=int(idd)))
  return(render_template("ticketpage.html", ticket = ticket, comments = comments,history=history, form = form))


#delete comments
@main.route("/tickets/comment/delete/<idd>/<c_id>")
@login_required
def delete_comment(idd, c_id):
  get_comment = Comment.query.get(int(c_id))
  db.session.delete(get_comment)
  db.session.commit()

  #add log to TH
  get_ticket = Ticket.query.get(int(idd))
  log = "deleted a comment"
  add_log(current_user.name,get_ticket,log)

  flash("comment deleted")
  return(redirect(url_for("main.view_ticket", idd = idd)))

#edit ticket
@main.route("/tickets/edit/<idd>", methods=["POST", "GET"])
@login_required
def edit_ticket(idd):
  get_ticket = Ticket.query.get(int(idd))
  #admin and project manager all access
  if current_user.role != "Developer":
    if request.method == "POST":
      title = request.form.get("title")
      description = request.form.get("description")
      assigned = request.form.get("assigned")
      priority = request.form.get("priority")
      status = request.form.get("status")
      ticket_type = request.form.get("type")

      #update
      if title:
        get_ticket.title = title
      if description:
        get_ticket.description= description
      if assigned != "N":
        get_ticket.assigned_dev = assigned
      if priority != "NONE":
        get_ticket.priority = priority
      if status != "N":
        get_ticket.status= status
      if ticket_type != "N":
        get_ticket.ticket_type  = ticket_type
      
      #add log to TH
      log="Edited this ticket"
      add_log(current_user.name, get_ticket,log)
      db.session.commit()
      flash('changes saved')
      return(redirect(url_for("main.view_ticket", idd=idd)))

    users = User.query.filter( or_(User.role == "Developer", User.role == "Project Manager")).all()
    return(render_template("editticket.html", ticket=get_ticket, users=users))
      

  #developer only status request(feature)

#delete tickets
@main.route("/tickets/delete/<idd>")
@login_required
def delete_ticket(idd):
  #for admin and project manager
  if current_user.role != "Developer":
    get_ticket = Ticket.query.get(int(idd))
    db.session.delete(get_ticket)
    db.session.commit()
    flash('Ticket deleted')
    return(redirect(url_for("main.mytickets")))
  flash('you dont have access to this request')
  return(redirect(url_for("main.mytickets")))




 

'''@main.route("/admin_/<idd>")
@login_required
def admin_(idd):
  try:
    items = Ticket.query.filter(Ticket.project_ticket.has(id=int(idd))).join(Ticket_history, Ticket_history.ticket_history.id == int(idd))

    return(render_template("admin.html", items = items))
  except:
    flash("code not working!")
    return(redirect(url_for("main.mytickets")))'''


#written by Wilfred 
