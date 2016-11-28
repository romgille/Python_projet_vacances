from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired
from wtforms import StringField, BooleanField, IntegerField
from wtforms.validators import DataRequired, InputRequired
from wtforms.fields.html5 import DateField
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('login', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

    remember_me = BooleanField('remember_me', default=False)

class PriseForm(FlaskForm):
	priseDateDebut = DateField('priseDateDebut', format='%d/%m/%Y')
	priseDateFin = DateField('priseDateFin', format='%d/%m/%Y')
	priseNbJours = IntegerField('priseNbJours',validators=[InputRequired()])

class DepotForm(FlaskForm):
	depotDateDebut = DateField('depotDateDebut', format='%d/%m/%Y')
	depotDateFin = DateField('depotDateFin', format='%d/%m/%Y')
	depotNbJours = IntegerField('depotNbJours', validators=[DataRequired()])


