from app import db

class User(db.Model):
	user_id = db.Column(db.Integer, primary_key=True)
	nom = db.Column(db.String(64), index=True, unique=True)
	prenom = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	resp_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	role = db.Column(db.Integer)

class Vacances(db.Model):
	date_debut = db.Column(db.DateTime)
	date_fin = db.Column(db.DateTime)
	nb_jour = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
	status = db.Column(db.Integer)
	

def __repr__(self):
	return '<User %r>' % (self.user_id)
