from flask import Flask, Blueprint, redirect, render_template, request, flash, url_for, session
from app.models import User
from app import db
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
from flask_wtf.file import FileField, FileAllowed
#from flask_uploads import IMAGES
#import random

main = Blueprint('main', __name__)
