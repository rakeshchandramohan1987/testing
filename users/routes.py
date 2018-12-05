from flask import render_template, url_for, flash, redirect, request, Blueprint, current_app
from flask_login import login_user, current_user, logout_user, login_required
from Glob import db, bcrypt
from Glob.models import User
from Glob.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                              ResetPasswordForm, RequestResetForm)
from Glob.users.utils import save_picture, send_reset_email, check_image
from datetime import datetime
import os
users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        username = form.firstname.data + ' ' + form.lastname.data
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data,
                    username=username, password=hashed_password, status='Created')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user == None:
            flash('You have not Registered. Please register', 'danger')
            return redirect(url_for('users.register'))
        if user and bcrypt.check_password_hash(user.password, form.password.data) and user.status == 'Deactivated':
            user.status = 'Created'
            user.updated_date = datetime.now()
            db.session.commit()
        if user.status == 'Suspended':
            flash('Login Unsuccessful. Your profile has been suspended', 'danger')
        elif user and bcrypt.check_password_hash(user.password, form.password.data) and user.status == 'Created':
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if check_image(picture_file) == True:
                flash('the image you uploaded is inapropriate, please choose another image', 'danger')
                return redirect(url_for('users.account'))
        current_user.image_file = picture_file
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.username = form.firstname.data + ' ' + form.lastname.data
        current_user.email = form.email.data
        current_user.occupation = form.occupation.data
        db.session.commit()

        flash(str(form.picture.data), 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.occupation.data = current_user.occupation
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)



@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('Please check your email for password reset link', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('The token is either invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
