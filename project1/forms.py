from flask_wtf import FlaskForm 
from wtforms import StringField,PasswordField,SubmitField, validators
from wtforms.validators import DataRequired , EqualTo

class UserRegistrationForm(FlaskForm):
    entryNumber = StringField('User Id',[validators.Length(min=6, max=25)])
    name = StringField('name',validators=[validators.Length(min=3, max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    emailId = StringField('Email Id',validators=[DataRequired()])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    name = StringField('Username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login') 

class BookIssuesForm(FlaskForm):
	userId = StringField('UserId', validators=[DataRequired()])
	submit = SubmitField('Issue Book')



