from flask import flash
from flask import redirect
from flask import render_template

from app import app
from app.forms import LoginForm
from app import db
from app.models import User


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html',
                           title='Home',
                           user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login and password requested for LDAP="%s", remember_me=%s' %
              (form.login.data, str(form.remember_me.data)))
        user_login = User.query.filter_by(nom=form.login.data).first()
        if user_login is None:
            user = User().create_user()
            db.session.add(user)
            db.session.commit()
        return redirect('/user/<user.nom>')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/user/<nom>')
def user(nom):
    user = User.query.filter_by(nom=nom).first()
    return render_template('index.html', user=user)
