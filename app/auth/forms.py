from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from ..models import User

class LoginForm(FlaskForm):
# the validator is needed because a string is required
    email = StringField("Email", validators=[DataRequired(), Length(min = 1, max = 64), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me on this site")
    submit = SubmitField("Submit")

class RegistrationForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Length(1,64),
                                    Email()])

    # don't want username to have _ or . 
    username = StringField('Username', validators=[
        DataRequired(),
        Length(1, 64),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                   'Usernames must have only letters, numbers, dots, or underscores',
        )])
    password = PasswordField('Password', validators=[
        DataRequired(),
        EqualTo('password_confirm', message='Passwords do not match.'
        )])
    password_confirm = PasswordField('Password (confirm):',
                                     validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry! Username already in use.')

class ChangePasswordForm(FlaskForm):
    """Form for changing password
    """
    old_password = PasswordField("Old Password", validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('new_password_confirm', message='Sorry, the passwords do not match.'
        )])
    new_password_confirm = PasswordField('Retype New Password:', validators=[DataRequired()])
    submit = SubmitField("Submit")