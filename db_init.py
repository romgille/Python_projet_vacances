#!flask/bin/python
from app import db
from app.models import User

u = User(user_id=1, login='redisj', nom='REDIS', prenom='Jean', email='jean.redis@esiee.fr', resp_id=1, role=1)
u1 = User(user_id=2, login='bertrang', nom='BERTRAND', prenom='Gilles', email='gilles.bertrand@esiee.fr', resp_id=2, role=1)
u2 = User(user_id=3, login='baudoing', nom='BAUDOIN', prenom='Geneviève', email='genevieve.baudoin@esiee.fr', resp_id=3, role=1)
u3 = User(user_id=4, login='lissorgg', nom='LISSORGUES', prenom='Gaelle', email='jgaelle.lissorgues@esiee.fr', resp_id=4, role=1)

db.session.add(u)
db.session.add(u1)
db.session.add(u2)
db.session.add(u3)

db.session.commit()
