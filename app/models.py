from app import db, login_manager
from app.forms import LoginForm
from app.ldap import Ldap


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(64), index=True, unique=True)
    nom = db.Column(db.String(64), index=True, unique=False)
    prenom = db.Column(db.String(64), index=True, unique=False)
    email = db.Column(db.String(120), index=True, unique=True)
    resp_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role = db.Column(db.Integer)

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

    def get_name(self):
        return self.nom

    @staticmethod
    def create_user():
        actual_user = Ldap.connect()
        if actual_user is not None:
            user = User(
                login=LoginForm().login.data,
                nom=actual_user[0],
                prenom=actual_user[1],
                email=actual_user[2],
                resp_id=actual_user[3],
                role=actual_user[4]
            )
            return user
        return None

    @property
    def is_authenticated(self):
        return True

    @property
    def is_resp(self):
        if self.resp_id >= 1:
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
