from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm



import os


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)
bootstrap = Bootstrap(app)

from app import views, models

