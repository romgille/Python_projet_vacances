from ldap3 import Connection
from ldap3 import Server, ALL, AUTH_SIMPLE, STRATEGY_SYNC

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

#os.environ["HTTP_PROXY"] = "http://cache.esiee.fr:3128"
#os.environ["HTTPS_PROXY"] = "http://cache.esiee.fr:3128"
#server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
#conn = Connection(server, user="uid=giller,ou=Users,dc=esiee,dc=fr", password='plop')

#print(conn)
#conn.open()
#conn.bind()
#print(conn.result)
#conn.unbind()

server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
conn = Connection(server)
conn.open()
conn.search('dc=esiee, dc=fr', '(&(objectclass=person)(uid=bercherj))',
        attributes=['sn', 'NumeroCCIP',  'idAurion', 'principalMail', 'googleMail',
            'telephoneNumber',  'displayName', 'roomNumber', 'givenName',
            'dateCreation', 'dateExpiration', 'annuairePresent', 'mailEDU', 'Name'])
print(conn.entries[0])
