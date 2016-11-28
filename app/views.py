from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from app import db,models
from .models import User

from app import app
from app.forms import LoginForm, DepotForm, PriseForm


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Foe'}  # fake user
    return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login and password requested for LDAP="%s", remember_me=%s' %
              (form.login.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form)

@app.route('/historique_validation_vacances')
def historique_admission_vacances():
    print(User.is_authenticated)
    list_vacances_users = models.User.query.filter_by(resp_id=1).all()
    l = []
    v = []
    for j in list_vacances_users:
        v = models.Vacances.query.filter_by(user_id=j.user_id, status=1).all()
        for n in v:
            l.append(n)
    print (len(l))
    if(len(l) > 0):
        msg = "Vacances autorisées"
    else:
        msg = "Il n'y a eu aucunes vacances autorisées."
    return render_template('historique_validation_vacances.html',
                           title='Historique',
                           l=l,
                           models=models,
                           msg=msg,
                           display=True)

@app.route('/admission_vacances',methods=['GET','POST'])
def admission_vacances():
    list_vacances_users = models.User.query.filter_by(resp_id=1).all()
    l = []
    v = []
    for j in list_vacances_users:
        v = models.Vacances.query.filter_by(user_id=j.user_id, status=0).all()
        for n in v:
            l.append(n)
    if(len(v) > 0):
        if(request.method == 'POST'):
            for i in request.form:
                result = request.form[i]
                if(result != "0"):
                    print ("ID Vacances : "+ i +" Rsultat : "+result)
                    u = models.Vacances.query.filter_by(vacances_id=i).first()
                    u.status = result
                    db.session.commit()

            msg = "Modification appliquées"

        else:
            msg="Appliquer les modifications nécessaires"

        return render_template('admission_vacances.html',
                               title='Autorisations',
                               l=l,
                               models=models,
                               msg=msg,
                               display=True)
    else:
        return render_template('admission_vacances.html',
                               title='Autorisations',
                               msg="Il n'y a pas de demandes de vancances.",
                               display=False
                               )

@app.route('/depot', methods=['GET', 'POST'])
def depot():
    form = DepotForm()
    if form.validate_on_submit():
        flash('Date de debut depot = "%s", Date de fin depot = "%s", Nb de jours depot=%s' %
              (str(form.depotDateDebut.data), str(form.depotDateFin.data),str(form.depotNbJours.data)))
        return redirect('/index')
    return render_template('depot.html',
                           title='Vacances - Depot',
                           form=form)

@app.route('/prise', methods=['GET', 'POST'])
def prise():
    form = PriseForm()
    if form.validate_on_submit():
        flash('Date de debut prise = "%s", Date de fin prise = "%s", Nb de jours prise=%s' %
              (str(form.priseDateDebut.data), str(form.priseDateFin.data),str(form.priseNbJours.data)))
        return redirect('/index')
    return render_template('prise.html',
                           title='Vacances - Prise',
                           form=form)
