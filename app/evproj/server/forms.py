from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, PasswordField, validators,
                     TextAreaField, RadioField, IntegerField)


class AuthForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])


class RegisterForm(FlaskForm):
    login = StringField('Login', [validators.DataRequired()])
    mail = StringField('Email', [validators.DataRequired()])
    name = StringField('Name', [validators.DataRequired()])
    surname = StringField('Surname', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    password_repeat = PasswordField('Password', [validators.DataRequired()])

class CreateEvent(FlaskForm):
    name = StringField('Name', [validators.DataRequired()])
    date_time = StringField('Date_time', [validators.DataRequired()])
