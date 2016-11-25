from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

import os


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)

from app import views, models

