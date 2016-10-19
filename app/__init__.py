#from ldap3 import Connection
#from ldap3 import Server, ALL

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_mail import Mail

import os


app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

mail = Mail(app)

from app import views, models


# os.environ["HTTP_PROXY"] = "http://cache.esiee.fr:3128"
# os.environ["HTTPS_PROXY"] = "http://cache.esiee.fr:3128"
# server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
# conn = Connection(server, user="uid=foe,ou=Users,dc=esiee,dc=fr", password='plop')
#
# print(conn)
# conn.open()
# conn.bind()
# print(conn)
# conn.unbind()

