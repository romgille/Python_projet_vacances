from flask import flash
from flask import redirect
from flask import render_template

from app import app
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"


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
