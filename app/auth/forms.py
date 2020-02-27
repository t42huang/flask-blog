from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, BooleanField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

from ..models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

def check_email_registered(form, field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email(), check_email_registered])
    username = StringField('Username', 
        validators=[DataRequired(), Length(1, 64), 
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                'Usernames must have only letters, numbers, dots or '
                'underscores')])
    password = PasswordField('Password', 
        validators=[DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[
        DataRequired(), Length(1, 64), Email(), check_email_registered,
        EqualTo('email2', message='Emails must match')
    ])
    email2 = StringField('Confirm Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    
    submit = SubmitField('Update')
            

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    
    submit = SubmitField('Update')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Length(1, 64), Email()
    ])
    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match')
    ])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Reset')