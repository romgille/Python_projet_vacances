from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)


init file (file app/__init__.py):


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
