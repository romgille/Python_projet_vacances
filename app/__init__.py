from ldap3 import Connection
from ldap3 import Server, ALL, AUTH_SIMPLE, STRATEGY_SYNC
from flask import Flask
from ldap3 import Server, ALL
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm

import os
import base64

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)
bootstrap = Bootstrap(app)

from app import views, models


os.environ["HTTP_PROXY"] = "http://cache.esiee.fr:3128"
os.environ["HTTPS_PROXY"] = "http://cache.esiee.fr:3128"
