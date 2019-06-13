from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,validators

class user_registration(FlaskForm):
    username = StringField('User Name')
    email = StringField('Email',[validators.Email("Please enter your email address.")])
    password = PasswordField('Password')
    re_enter_pass = PasswordField('Re-Enter Password')
    submit = SubmitField('Sign up')

class user_login(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Sign in')

class forget_password_form(FlaskForm):
    mail_id =StringField('Please use registered mail id')
    submit = SubmitField('send link to forget password')
class new_password(FlaskForm):
    pass1 =PasswordField('New Password')
    re_enter =PasswordField('New Password')
    submit = SubmitField('save')