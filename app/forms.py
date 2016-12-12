from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import StringField, BooleanField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class PriseForm(FlaskForm):
    priseDateDebut = DateField('priseDateDebut', format='%d/%m/%Y')
    priseDateFin = DateField('priseDateFin', format='%d/%m/%Y')
    priseNbJours = IntegerField('priseNbJours', validators=[InputRequired()])


class DepotForm(FlaskForm):
    depotDateDebut = DateField('depotDateDebut', format='%d/%m/%Y')
    depotDateFin = DateField('depotDateFin', format='%d/%m/%Y')
    depotNbJours = IntegerField('depotNbJours', validators=[DataRequired()])
