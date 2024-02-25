from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField,EmailField,PasswordField)
from wtforms.validators import InputRequired, Length,Email,Regexp,EqualTo
# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'

def validate_email_domain(form, field):
    email = field.data
    allowed_domains = ['gmail.com', 'hotmail.com','cmu.ac.th']
    domain = email.split('@')[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Invalid email domain. Allowed domains are: {", ".join(allowed_domains)}')
class RegistrationForm(FlaskForm):
    name = StringField('name', validators=[
        InputRequired(message="name is required"),
        Length(min=2, max=20, message="name must be between 2 and 20 characters long")
    ])
    email = EmailField('email', validators=[
        InputRequired(message="Email is required mush be *@gmail.com or *@hotmail.com or *@cmu.ac.th" ),
        validate_email_domain
    ])
    password = PasswordField('password', validators=[
        InputRequired(message="Password is required"),
        Regexp("r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%^&+=])(?=\S+$).{8,}$'", message="Password must contain at least one number"),
        Length(min=8, message="Password must contain at least 8 characters including at least one digit, one lowercase letter, one uppercase letter, and one special character")
    ])
