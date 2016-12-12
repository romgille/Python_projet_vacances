import base64

import re

import csv

from ldap3 import Connection, ALL
from ldap3 import Server

from app import models
from app.forms import LoginForm


class Ldap:
    @staticmethod
    def connect():
        server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
        first_conn = Connection(server, user="uid=" + LoginForm().login.data + ",ou=Users,dc=esiee,dc=fr",
                                password=LoginForm().password.data)
        first_conn.open()
        first_conn.search('dc=esiee, dc=fr', "(&(objectclass=person)(uid=" + LoginForm().login.data + "))",
                          attributes=['sn', 'principalMail', 'googleMail',
                                      'telephoneNumber', 'displayName', 'roomNumber', 'givenName',
                                      'dateCreation', 'dateExpiration', 'annuairePresent', 'mailEDU', 'Name'])
        if len(first_conn.entries) > 0:
            name = base64.b64decode(str(first_conn.entries[0]['Prenom'])).decode('UTF-8')
            surname = base64.b64decode(str(first_conn.entries[0]['Nom'])).decode('UTF-8')
            email = str(first_conn.entries[0]['googleMail'])

            dept_resp = create_dic_with_department()
            usr_resp = create_dic_with_user(dept_resp)
            resp_id = models.User.query.filter_by(user_id=usr_resp[LoginForm().login.data]).first().get_id()
            role = 0
            user = [surname, name, email, resp_id, role]
            first_conn.bind()
            return user
        first_conn.bind()
        return None

    @staticmethod
    def connect_simple():
        server = Server('ldap.esiee.fr', use_ssl=True, get_info=ALL)
        first_conn = Connection(server, user="uid=" + LoginForm().login.data + ",ou=Users,dc=esiee,dc=fr",
                                password=LoginForm().password.data)
        first_conn.open()
        return first_conn.bind()


def create_dic_with_department():
    dept_resp = {}
    with open('csv/resp_depts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == 'dept':
                dept = row[1].strip()
                name = row[3].strip()
                firstname = row[2].strip()
                login = re.sub('[éèê]', 'e', (name[:8] + firstname[0]).lower())
                dept_resp[dept] = login
    return dept_resp


def create_dic_with_user(dept_resp):
    dept_usr = {}
    with open('csv/liste_enseignants_2016-17.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            name = re.search('([A-Z\']|( [A-Z]{2,}))+', row[0]).group(0).strip()
            firstname = row[0].split(name)[1].strip()
            login = re.sub('[éèê]', 'e', (name[:8] + firstname[0]).lower())  # TODO : check more special chars
            # print(row[1].split('EP : Dept. ')[1])
            resp = dept_resp[row[1].split('EP : Dept. ')[1]]
            dept_usr[login] = resp
    return dept_usr
