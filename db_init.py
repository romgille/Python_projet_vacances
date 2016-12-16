#!flask/bin/python
from app import db
from app.models import User
import csv
import re

def import_resp_to_db(i):
    with open('csv/resp_depts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        user_id=0
        for row in reader:
            user_id+=1
            if row[0] == 'dept':
                name = row[3].strip()
                firstname = row[2].strip()
                login = re.sub('[éèê]', 'e', (name[0:8] + firstname[0]).lower())
                email = row[4].strip()
                role=1
                u = User(user_id=user_id, login=login, nom=name, prenom=firstname, email=email, resp_id=user_id, role=role)
                db.session.add(u)

    db.session.commit()                


def get_department(i):
    dept_dic = {}
    with open('csv/resp_depts.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] == 'dept':
                name = row[3].strip()
                firstname = row[2].strip()
                dept = row[1].strip()
                login = re.sub('[éèê]', 'e', (name[0:8] + firstname[0]).lower())
                dept_dic[dept]  = login
    return dept_dic


def import_user_to_db(i):
    with open('csv/liste_enseignants_2016-17.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        dept_dic = get_department(i)
        for row in reader:
            name = row[0].split(" ")[0]
            firstname = row[0].split(" ")[1]
            login = re.sub('[éèê]', 'e', (name[0:8] + firstname[0]).lower())
            email = firstname + "." + name + "@esiee.fr" 
            role=1
            dept = row[1].split('EP : Dept. ')[1]
            resp_id = dept_dic[dept]
            u = User(login=login, nom=name, prenom=firstname, email=email, resp_id=resp_id, role=role)
            if(User.query.filter_by(login=login).first() is None):
                db.session.add(u)
    db.session.commit()

import_resp_to_db(0)
import_user_to_db(0)
