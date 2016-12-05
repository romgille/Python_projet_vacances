from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
import time
from flask import url_for
from flask_login import logout_user, login_required, login_user

from app import app
from app import db, models
from app.forms import LoginForm, DepotForm, PriseForm
from app.models import User
from app import utils
from app.utils.mail import Mail


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print('Login and password requested for LDAP="%s", remember_me=%s' %
              (form.login.data, str(form.remember_me.data)))
        actual_user = User.query.filter_by(login=form.login.data).first()
        if not actual_user:
            actual_user = User(form.login.data).create_user()
            db.session.add(actual_user)
            db.session.commit()
        login_user(actual_user)
        return redirect('/user/' + form.login.data)
    return render_template('login.html',
                           title='Sign Up',
                           form=form)


@app.route('/historique_validation_vacances')
@login_required
def historique_admission_vacances():
    print(User.is_authenticated)
    list_vacances_users = models.User.query.filter_by(resp_id=1).all()
    l = []
    for j in list_vacances_users:
        v = models.Vacances.query.filter_by(user_id=j.user_id, status=1).all()
        for n in v:
            l.append(n)
    print(len(l))
    if len(l) > 0:
        msg = "Vacances autorisées"
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
    print(User().is_authenticated)
    list_vacances_users = models.User.query.filter_by(resp_id=1).all()
    l = []
    v = []
    for j in list_vacances_users:
        v = models.Vacances.query.filter_by(user_id=j.user_id, status=0).all()
        for n in v:
            l.append(n)
    if len(v) > 0:
        if request.method == 'POST':
            for i in request.form:
                result = request.form[i]
                if result != "0":
                    print("ID Vacances : " + i + " Rsultat : " + result)
                    u = models.Vacances.query.filter_by(vacances_id=i).first()
                    u.status = result
                    db.session.commit()

            msg = "Modifications appliquées"

        else:
            msg = "Appliquer les modifications nécessaires"

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


@app.route('/depot', methods=['GET', 'POST'])
@login_required
def depot():
    form = DepotForm()
    if form.validate_on_submit():
        flash('Date de debut depot = "%s", Date de fin depot = "%s", Nb de jours depot=%s' %
              (str(form.depotDateDebut.data), str(form.depotDateFin.data), str(form.depotNbJours.data)))
        user = None # TODO : fletch User (from session ?)
        models.Vacances.depot_vacances(form.depotDateDebut.data,form.depotDateFin.data,form.depotNbJours.data,user)
        Mail.vacation_notification (user, [form.depotDateDebut.data,form.depotDateFin.data], Mail.notification_type.add_vacation)
        return redirect('/index')
    return render_template('depot.html',
                           title='Vacances - Depot',
                           form=form)


@app.route('/prise', methods=['GET', 'POST'])
@login_required
def prise():
    form = PriseForm()
    if form.validate_on_submit():
        flash('Date de debut prise = "%s", Date de fin prise = "%s", Nb de jours prise=%s' %
              (str(form.priseDateDebut.data), str(form.priseDateFin.data), str(form.priseNbJours.data)))
        user = None # TODO : fletch User (from session ?)
        Mail.vacation_notification (user, [form.depotDateDebut.data,form.depotDateFin.data], Mail.notification_type.remove_vacation)
        return redirect('/index')
    return render_template('prise.html',
                           title='Vacances - Prise',
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
