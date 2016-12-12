#!flask/bin/python

import csv
import re

from app import db, models
from app.ldap import Ldap


dept_resp = {}
with open ('csv/resp_depts.csv', 'r') as csvfile :
    reader = csv.reader (csvfile, delimiter=',')
    for row in reader :
        if row[0] == 'dept' :
            dept = row[1].strip()
            name = row[3].strip()
            firstname =  row[2].strip()
            #email = row[4].strip()
            login = re.sub('[éèê]', 'e', (name[:8] + firstname[0]).lower()) # TODO : check more special chars
            user_data = Ldap.createUserFromLoginWithoutPass(login)
            user = models.User(
                login=login,
                nom=user_data[0],
                prenom=user_data[1],
                email=user_data[2],
                resp_id=0,
                role=0)
            db.session.add(user)
            dept_resp[dept] = user

with open ('csv/liste_enseignants_2016-17.csv', 'r') as csvfile :
    reader = csv.reader (csvfile, delimiter=',')
    for row in reader :
        name = re.search ('([A-Z\']|( [A-Z]{2,}))+', row[0]).group(0).strip()
        firstname = row[0].split (name)[1].strip()
        login = re.sub('[éèê]', 'e', (name[:8] + firstname[0]).lower()) # TODO : check more special chars
        resp = dept_resp[ row[1].split ('EP : Dept. ')[1] ]
        user_data = Ldap.createUserFromLoginWithoutPass(login)
        user = models.User (
            login=login,
            nom=user_data[0],
            prenom=user_data[1],
            email=user_data[2],
            resp_id=resp.user_id,
            role=0)
        db.session.add(user)

db.session.commit()


