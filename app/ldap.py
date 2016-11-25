import base64

from ldap3 import Connection, ALL
from ldap3 import Server


class Ldap:
    @staticmethod
    def check_login():
        server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
        first_conn = Connection(server, user="uid=user,ou=Users,dc=esiee,dc=fr", password='password')
        first_conn.open()
        first_conn.bind()

        if first_conn.result['description'] == 'success':

            conn = Connection(server)
            conn.open()
            conn.search('dc=esiee, dc=fr', "(&(objectclass=person)(uid=giller))",
                        attributes=['sn', 'principalMail', 'googleMail',
                                    'telephoneNumber', 'displayName', 'roomNumber', 'givenName',
                                    'dateCreation', 'dateExpiration', 'annuairePresent', 'mailEDU', 'Name'])
            name = base64.b64decode(str(conn.entries[0]['Prenom'])).decode('UTF-8')
            surname = base64.b64decode(str(conn.entries[0]['Nom'])).decode('UTF-8')
            email = "plop@yopmail.com"  # base64.b64decode(str(conn.entries[0]['googleMail'])).decode('UTF-8')
            resp_id = 1  # Todo faire propre
            role = 0  # Todo faire propre
            is_student = False
            #if conn.entries[0]['mailEDU'].decode('UTF-8') == 'N':
            #    is_student = False

            if is_student:
                print('Bad Credentials')  # TODO créer une page pour login student
                return

            user = [name, surname, email, resp_id, role]

            return user

        else:
            print('Bad Credentials')

        first_conn.unbind()
