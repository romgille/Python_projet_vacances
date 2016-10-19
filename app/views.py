from flask import flash
from flask import redirect
from flask import render_template

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

@app.route('/depot', methods=['GET', 'POST'])
def depot():
    form = DepotForm()
    if form.validate_on_submit():
        flash('Date de debut depot = "%s", Date de fin depot = "%s", Nb de jours depot=%s' %
              (str(form.depotDateDebut), str(form.depotDateFin.data),str(form.depotNbJours.data)))
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
