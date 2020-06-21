from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()


def create_app():
  app = Flask(__name__)

  app.config['SECRET_KEY'] = 'ASpire2begreat'
  app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://xczqgmpzkonwkf:1abc0c71a01357e5c8d9aa421e3d1a119f34d2385bb13553873a4bbd538afc1b@ec2-54-86-170-8.compute-1.amazonaws.com:5432/d35kj3mpcd9svj"
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

  db.init_app(app)
  from app.models import User, Project, Ticket, Comment,Ticket_history
  migrate.init_app(app, db)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  from app.models import User

  @login_manager.user_loader
  def load_user(user_id):
    return(User.query.get(int(user_id)))


  # blueprint for auth routes in our app
  from app.forms import forms as forms_blueprint
  app.register_blueprint(forms_blueprint)

  # blueprint for non-auth parts of app
  from app.main import main as main_blueprint
  app.register_blueprint(main_blueprint)

  return(app)
