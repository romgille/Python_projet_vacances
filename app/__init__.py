from ldap3 import Connection
from ldap3 import Server, ALL, AUTH_SIMPLE, STRATEGY_SYNC
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import base64

app = Flask(__name__)

app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

login = 'giller'

server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
first_conn = Connection(server, user="uid=" + login + ",ou=Users,dc=esiee,dc=fr", password='')
first_conn.open()
first_conn.bind()

if first_conn.result['description'] == 'success':
    
    conn = Connection(server)
    conn.open()
    conn.search('dc=esiee, dc=fr', "(&(objectclass=person)(uid=" + login + "))",
            attributes=['sn', 'principalMail', 'googleMail',
                'telephoneNumber',  'displayName', 'roomNumber', 'givenName',
                'dateCreation', 'dateExpiration', 'annuairePresent', 'mailEDU', 'Name'])
    name     = base64.b64decode(str(conn.entries[0]['Prenom'])).decode('UTF-8')
    surname = base64.b64decode(str(conn.entries[0]['Nom'])).decode('UTF-8')
    print(name)
    print(surname)
    #print(conn.entries[0])

else:
    print('Bad Credentials')

first_conn.unbind()
