from app import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), index=True, unique=True)
    prenom = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    resp_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    role = db.Column(db.Integer)

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
	def depotVacances(datedebut, datefin, nbjour, user):
		u=Vacances(date_debut=datedebut, date_fin=datefin, nb_jour=nbjour, user_id=user, status=0)
		db.session.add(u)
		db.session.commit()

	@staticmethod
	def priseVacances(datedebut, datefin, nbjour, user):
		u=Vacances(date_debut=datedebut, date_fin=datefin, nb_jour=-nbjour, user_id=user, status=0)
		db.session.add(u)
		db.session.commit()

