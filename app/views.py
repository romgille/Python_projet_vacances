from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_login import logout_user, login_required, login_user

from app import app
from app import db, models
from app.forms import LoginForm, DepotForm, PriseForm
from app.ldap import Ldap
from app.models import User
from app.utils.mail import Mail
from app.utils.dbmethods import DbMethods


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if Ldap.connect_simple():
            u = User.query.filter_by(login=form.login.data).first()
            #if not u:
            #    u = User.create_user()
            #    db.session.add(u)
            #    db.session.commit()
            login_user(u)
            session["user_id"] = u.get_id()
            session["role"] = u.role
            return redirect('/user/' + form.login.data)
    return render_template('login.html',
                           title='Sign Up',
                           form=form)


@app.route('/historique_validation_vacances')
@login_required
def historique_admission_vacances():
    resp_id = session.get("user_id", None)
    if models.User.query.filter_by(user_id=resp_id).first().role >= 1:
        list_vacances_users = models.User.query.filter_by(resp_id=resp_id).all()
        l = []
        for j in list_vacances_users:
            v = models.Vacances.query.filter(models.Vacances.user_id == j.user_id, models.Vacances.status != 0).all()
            for n in v:
                l.append(n)
        print(len(l))
        if len(l) > 0:
            msg = "Historique des vacances"
        else:
            msg = "Il n'y a eu aucunes vacances autorisées."
        return render_template('historique_validation_vacances.html',
                               title='Historique',
                               l=l,
                               models=models,
                               msg=msg,
                               display=True)
    else:
        return render_template('historique_validation_vacances.html',
                               title='Interdit',
                               models=models,
                               msg="Vous n'avez pas les droits nécessaires pour accéder à cette page.",
                               display=False)


@app.route('/historique_user')
@login_required
def historique_user():
    user_id = session.get("user_id", None)
    l = []
    v = models.Vacances.query.filter(models.Vacances.user_id == user_id, models.Vacances.status != 0).all()
    for n in v:
        l.append(n)
    print(len(l))
    if len(l) > 0:
        msg = "Historique des vacances"
    else:
        msg = "Il n'y a eu aucunes vacances autorisées."
    return render_template('historique_validation_vacances.html',
                           title='Historique',
                           l=l,
                           models=models,
                           msg=msg,
                           display=True)


@app.route('/admission_vacances', methods=['GET', 'POST'])
@login_required  # TODO resp
def admission_vacances():
    resp_id = session.get("user_id", None)
    if models.User.query.filter_by(user_id=resp_id).first().role >= 1:
        if request.method == 'POST':
            for i in request.form:
                result = request.form[i]
                if result != "0":
                    print("ID Vacances : " + i + " Resultat : " + result)
                    u = models.Vacances.query.filter_by(vacances_id=i).first()
                    u.status = result
                    db.session.commit()
                msg = "Modifications appliquées"
        else:
            msg = "Appliquer les modifications nécessaires"

        list_vacances_users = models.User.query.filter_by(resp_id=resp_id).all()
        l = []
        v = []
        for j in list_vacances_users:
            v = models.Vacances.query.filter_by(user_id=j.user_id, status=0).all()
            for n in v:
                l.append(n)
        if len(v) > 0:

            return render_template('admission_vacances.html',
                                   title='Autorisations',
                                   l=l,
                                   models=models,
                                   msg=msg,
                                   display=True)
        else:
            return render_template('admission_vacances.html',
                                   title='Autorisations',
                                   msg="Il n'y a pas de demande de vacances.",
                                   display=False
                                   )
    else:
        return render_template('admission_vacances.html',
                               title="Interdit",
                               msg="Vous n'avez pas les droits nécessaires pour accéder à cette page.",
                               display=False
                               )


@app.route('/depot', methods=['GET', 'POST'])
@login_required
def depot():
    form = DepotForm()
    user_id = session.get('user_id', None)
    user = models.load_user(user_id)
    v = models.Vacances.query.filter(models.Vacances.user_id == user_id, models.Vacances.status == 1).all()
    w = models.Vacances.query.filter(models.Vacances.user_id == user_id, models.Vacances.status == 0).all()

    solde_vacances = 0
    if len(v) > 0:
        for i in v:
            solde_vacances = solde_vacances + i.nb_jour

    solde_vacances_validation = solde_vacances
    if len(w) > 0:
        for j in w:
            solde_vacances_validation = solde_vacances_validation + j.nb_jour

    if form.validate_on_submit():
        DbMethods.depot_vacances(user_id, form.depotDateDebut.data, form.depotDateFin.data, form.depotNbJours.data)
        Mail.vacation_notification(user, [form.depotDateDebut.data, form.depotDateFin.data],
                                   Mail.notification_type.add_vacation)
        return redirect('/index')
    return render_template('depot.html',
                           title='Vacances - Depot',
                           solde_vacances=solde_vacances,
                           solde_vacances_validation=solde_vacances_validation,
                           form=form)


@app.route('/prise', methods=['GET', 'POST'])
@login_required
def prise():
    form = PriseForm()
    user_id = session.get('user_id', None)
    user = models.load_user(user_id)
    v = models.Vacances.query.filter(models.Vacances.user_id == user_id, models.Vacances.status == 1).all()
    w = models.Vacances.query.filter(models.Vacances.user_id == user_id, models.Vacances.status == 0).all()

    solde_vacances = 0
    if len(v) > 0:
        for i in v:
            solde_vacances = solde_vacances + i.nb_jour

    solde_vacances_validation = solde_vacances
    if len(w) > 0:
        for j in w:
            solde_vacances_validation = solde_vacances_validation + j.nb_jour

    if form.validate_on_submit():
        DbMethods.prise_vacances(user_id, form.priseDateDebut.data, form.priseDateFin.data, form.priseNbJours.data)
        Mail.vacation_notification(user, [form.priseDateDebut.data, form.priseDateFin.data],
                                   Mail.notification_type.remove_vacation)
        return redirect('/index')
    return render_template('prise.html',
                           title='Vacances - Prise',
                           solde_vacances=solde_vacances,
                           solde_vacances_validation=solde_vacances_validation,
                           form=form)


@app.route('/user/<user_login>', methods=['GET', 'POST'])
@login_required
def user(user_login):
    actual_user = User.query.filter_by(login=user_login).first()
    nom = actual_user.nom
    prenom = actual_user.prenom
    return render_template('user.html',
                           nom=prenom + ' ' + nom)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.errorhandler(401)
def unauthorized(e):
    return render_template('401.html'), 401


@app.errorhandler(404)
def unauthorized(e):
    return render_template('404.html'), 404
