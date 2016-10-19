import base64

from ldap3 import Connection, ALL
from ldap3 import Server
from app.forms import LoginForm

login = LoginForm.login
password = LoginForm.password

server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
first_conn = Connection(server, user="uid=" + login + ",ou=Users,dc=esiee,dc=fr", password='')
first_conn.open()
first_conn.bind()

if first_conn.result['description'] == 'success':

    conn = Connection(server)
    conn.open()
    conn.search('dc=esiee, dc=fr', "(&(objectclass=person)(uid=" + login + "))",
                attributes=['sn', 'principalMail', 'googleMail',
                            'telephoneNumber', 'displayName', 'roomNumber', 'givenName',
                            'dateCreation', 'dateExpiration', 'annuairePresent', 'mailEDU', 'Name'])
    name = base64.b64decode(str(conn.entries[0]['Prenom'])).decode('UTF-8')
    surname = base64.b64decode(str(conn.entries[0]['Nom'])).decode('UTF-8')
    email = conn.entries[0]['googleMail'].decode('UTF-8')
    isStudent = True
    if conn.entries[0]['mailEDU'].decode('UTF-8') == 'N':
        isStudent = False
    print(name)
    print(surname)
    print(isStudent)
else:
    print('Bad Credentials')

first_conn.unbind()
