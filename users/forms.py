_author_ = 'Rakesh Chandramohan'

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Glob.models import User


class RegistrationForm(FlaskForm):
    firstname = StringField('Firstname*',
                           validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname*',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email*',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password*',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('Firstname',
                            validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname',
                           validators=[DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    occupation = StringField('Occupation',
                             validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')



class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField(' Password Reset Request')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no email with email provided.' )


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password*', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password*',
                                     validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Reset Password')