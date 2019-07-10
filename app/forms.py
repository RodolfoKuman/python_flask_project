from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField
from wtforms.fields.html5 import EmailField

from .models import User

def codi_validator(formulario, field):
    if field.data == 'codi' or field.data == 'Codi':
        raise validators.ValidationError('El username codi no es permitido.')

def length_honeypot(form, field):
    if len(field.data) > 0:
        raise validators.ValidationError('Solo los humanos pueden completar el registro!')

class LoginForm(Form):
    username = StringField('Username', [
        validators.length(min=4, max=50, message='El usuario se encuentra fuera de rango')
    ])
    password = PasswordField('Password',[
        validators.Required()
    ])

class RegisterForm(Form):
    honeypot = HiddenField("", [ length_honeypot ])

    username = StringField('Username', [
        validators.length(min=4, max=50, message='El usuario se encuentra fuera de rango'),
        codi_validator
    ])
    email = EmailField('Correo electronico', [
        validators.length(min=6, max=100),
        validators.Required(message='El email es requerido.'),
        validators.email(message='Ingrese un email valido')
    ])
    password = PasswordField('Password',[
        validators.Required('La contraseña es requerida'),
        validators.EqualTo('confirm_password', message='La contraseña no coincide')

    ])
    confirm_password = PasswordField('Confirm password')
    accept = BooleanField('', [
        validators.DataRequired()
    ])

    def validate_username(self, username):
        if User.get_by_username(username.data):
            raise validators.ValidationError('El usuario ya se encuentra en uso')

    def validate_email(self, email):
        if User.get_by_email(email.data):
            raise validators.ValidationError('El email ya se encuentra en uso')
