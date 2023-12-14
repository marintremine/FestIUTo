"""
Application forms
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, validators, EmailField


class RegistrationForm(FlaskForm):
    """Form for registering a user"""
    username = StringField('Username', [validators.Length(min=1, max=25, message="Username must be between 1 and 25 characters")])
    password = PasswordField('Password', [validators.Length(min=8, max=256, message="Password must be between 8 and 256 characters")])
    remember_me = BooleanField('Remember Me', default=False)

class LoginForm(FlaskForm):
    """Form for logging in a user"""
    email = EmailField('Email', [validators.Length(min=1, max=256, message="Email must be between 1 and 256 characters")])
    password = PasswordField('Password', [validators.Length(min=8, max=256, message="Password must be between 8 and 256 characters")])
    remember_me = BooleanField('Remember Me', default=False)