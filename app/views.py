from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from app import db,models

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

@app.route('/admission_vacances',methods=['GET','POST'])
def admission_vacances():
    if(request.method == 'POST'):
        msg = request.form
        return render_template('admission_vacances.html',title="ok",msg=msg)
    else:
        msg="Appliquer les modifications nécessaires"
        u=models.User.query.filter_by(resp_id=1).all()
        l=[]
        v=[]
        for j in u:
            v=models.Vacances.query.filter_by(user_id=j.user_id,status=0).all()
            for n in v:
                l.append(n)


        return render_template('admission_vacances.html',
                               title='Autorisations',
                               l=l,
                               models=models,
                               msg=msg)


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
