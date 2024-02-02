from flask_wtf import FlaskForm
from wtforms import (EmailField,PasswordField)
from wtforms.validators import InputRequired, Length,Email,Regexp,EqualTo

class registerForm(FlaskForm):
    email = EmailField('Email',validators=[InputRequired(),Email(message="Invalid Email")])
    password = PasswordField('Password', validators=[InputRequired(),Regexp(".*[0-9].*",message="Password must contain at least one number"),Length(min=1)])
    confirm_password = PasswordField('Confirm Password',validators=[InputRequired(),EqualTo("password","Passwords must match")])
                       
    