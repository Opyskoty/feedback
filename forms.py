"""Forms for app."""

from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """Form for registration."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
    email = StringField("Email", validators=[InputRequired(), Email()])
    first_name = StringField("First name", validators=[
                             InputRequired(), Length(min=1, max=30)])
    last_name = StringField("Last name", validators=[
                            InputRequired(), Length(min=1, max=30)])


class LoginForm(FlaskForm):
    """Form for login."""

    username = StringField("Username", validators=[
                           InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[
                             InputRequired(), Length(min=8)])
