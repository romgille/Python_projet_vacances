from flask import flash
from flask import redirect
from flask import render_template

from app import app
from app.forms import LoginForm
from app import db,models


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
