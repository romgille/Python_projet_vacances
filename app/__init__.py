from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

from flask_bootstrap import Bootstrap


import os


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)
bootstrap = Bootstrap(app)

from app import views, models, forms, ldap


os.environ["HTTP_PROXY"] = "http://cache.esiee.fr:3128"
os.environ["HTTPS_PROXY"] = "http://cache.esiee.fr:3128"
