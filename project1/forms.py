from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired , EqualTo

class UserRegistrationForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    contact = StringField('contact',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    confirm_password = PasswordField('contact',validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login') 




