from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from app import app
from app.forms import LoginForm
from app import db
from app.models import User


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
            user = User().create_user()
            db.session.add(user)
            db.session.commit()
        return redirect('/user/' + user_login)
    return render_template('login.html',
                           title='Sign In',
                           form=form)


# @app.route('/user/<nom>')
# def user(nom):
#     user_nom = User.query.filter_by(nom=nom).first()
#     return render_template('index.html', nom=user_nom)

@app.route('/user/<user_login>')
def user(user_login):
    user = User.query.filter_by(login=user_login).first()
    nom = user.nom
    prenom = user.prenom
    return render_template('user.html',
                           nom=prenom + ' ' + nom)
