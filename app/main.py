from flask import Blueprint, redirect, render_template, request, flash, url_for
from app.models import User
from app import db
from flask_wtf import FlaskForm
#from flask_wtf.file import FileField, FileAllowed
#from flask_uploads import IMAGES
#import random

main = Blueprint('main', __name__)


@main.route("/")
def home():
  pass