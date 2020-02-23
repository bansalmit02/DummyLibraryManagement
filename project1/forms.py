from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired , EqualTo

class UserRegistrationForm(FlaskForm):
    entryNumber = StringField('Entry Number',validators=[DataRequired()])
    name = StringField('name',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    emailId = StringField('Email Id',validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login') 




