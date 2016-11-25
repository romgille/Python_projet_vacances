from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from app import db,models

from app import app
from app.forms import LoginForm
from app import db
from app.models import User
from app.forms import LoginForm, DepotForm, PriseForm
from app import db,models


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
        exists = db.session.query(db.session.query(User).filter_by(login=form.login.data).exists()).scalar()
        user_login = form.login.data
        if not exists:
            actual_user = User().create_user()
            db.session.add(actual_user)
            db.session.commit()
        return redirect('/user/' + user_login)
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


# @app.route('/user/<nom>')
# def user(nom):
#     user_nom = User.query.filter_by(nom=nom).first()
#     return render_template('index.html', nom=user_nom)

@app.route('/user/<user_login>')
def user(user_login):
    actual_user = User.query.filter_by(login=user_login).first()
    nom = actual_user.nom
    prenom = actual_user.prenom
    return render_template('user.html',
                           nom=prenom + ' ' + nom)

@app.route('/admission_vacances',methods=['GET','POST'])
def admission_vacances():
    u=models.User.query.filter_by(resp_id=1).all()
    l=[]
    v=[]
    for j in u:
        v=models.Vacances.query.filter_by(user_id=j.user_id,status=0).all()
        for n in v:
            l.append(n)
    print (l[0].user_id)


    return render_template('admission_vacances.html',
                           title='Autorisations',
                           l=l,
                           models=models)
