from ldap3 import Connection
from ldap3 import Server, ALL

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
conn = Connection(server, user="uid=bercherj,ou=Users,dc=esiee,dc=fr", password='bonjour')

print(conn)
conn.open()
conn.bind()
print(conn.result)
conn.unbind()
