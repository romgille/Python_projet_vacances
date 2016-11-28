from app import db
from app.ldap import Ldap
from app.forms import LoginForm
from app.forms import LoginForm
from app.ldap import Ldap


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(64), index=True, unique=True)
    nom = db.Column(db.String(64), index=True, unique=False)
    prenom = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    resp_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role = db.Column(db.Integer)
    
    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return ord(self.id)
        except NameError:
            return str(self.id)

    def get_name(self):
        return self.nom

    def create_user(self):
        actual_user = Ldap.check_login()
        self.login = LoginForm().login.data
        self.nom = actual_user[0]
        self.prenom = actual_user[1]
        self.email = actual_user[2]
        self.resp_id = actual_user[3]
        self.role = actual_user[4]
        return self

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return ord(self.id)
        except NameError:
            return str(self.id)

    def get_name(self):
        return self.nom

    def create_user(self):
        actual_user = Ldap.check_login()
        self.login = LoginForm().login.data
        self.nom = actual_user[0]
        self.prenom = actual_user[1]
        self.email = actual_user[2]
        self.resp_id = actual_user[3]
        self.role = actual_user[4]
        return self

    @property
    def is_authenticated(self):
        return True
    @property
    def is_resp(self):
        if(self.resp_id >=1):
            return True
        else:
            return False

    def __repr__(self):
        return '<User %r>' % self.user_id


class Vacances(db.Model):
    vacances_id = db.Column(db.Integer, primary_key=True)
    date_debut = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    nb_jour = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    status = db.Column(db.Integer)

    def __repr__(self):
        return '<Vacances %r>' % self.vacances_id

    @staticmethod
    def depot_vacances(datedebut, datefin, nbjour, user):
        u = Vacances(date_debut=datedebut, date_fin=datefin, nb_jour=nbjour, user_id=user, status=0)
        db.session.add(u)
        db.session.commit()

    @staticmethod
    def prise_vacances(datedebut, datefin, nbjour, user):
        u = Vacances(date_debut=datedebut, date_fin=datefin, nb_jour=-nbjour, user_id=user, status=0)
        db.session.add(u)
        db.session.commit()
