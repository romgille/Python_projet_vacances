from app import db
from app.models import Vacances


class DbMethods:
    # depot_vacances
    # 
    # @param user User : user reference
    # @param date_debut TYPE? : bla
    # @param date_fin TYPE? : bla
    # @param nb_jour integer : bla
    @staticmethod
    def depot_vacances(user, date_debut, date_fin, nb_jour):
        v = Vacances(
            date_debut=date_debut,
            date_fin=date_fin,
            nb_jour=nb_jour,
            user_id=user,
            status=0)
        db.session.add(v)
        db.session.commit()

    # prise_vacances
    # 
    # @param user User : user reference
    # @param date_debut TYPE? : bla
    # @param date_fin TYPE? : bla
    # @param nb_jour integer : bla
    @staticmethod
    def prise_vacances(user, datedebut, datefin, nbjour):
        v = Vacances(
            date_debut=datedebut,
            date_fin=datefin,
            nb_jour=-nbjour,
            user_id=user,
            status=0)
        db.session.add(v)
        db.session.commit()
