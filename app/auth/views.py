import email
from flask import render_template, session, g, redirect, url_for, flash, current_app, request

# from app.email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm # need a period because trying to import within package
from .. import db
from ..models import User, Role
from flask_login import login_required, logout_user, login_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from . import auth


@auth.route('/login' , methods=["GET", "POST"])
def login():
    # form is created
    form = LoginForm()

    """email_entered = form.email.data
    password_entered = form.password.data
    # query checking if the name is in the database
    user = User.query.filter_by(email = email_entered).first()
    # if user exists and the password is correct
    if user and user.verify_password(password_entered):
        login_user(user, form.remember_me.data)
        next = request.args.get('next')

        if next is None or not next.startswith('/'):
            next = url_for('main.index')
        return redirect(next)
        # flash a message that username/password is invalid
    flash("The username/password is invalid")"""


    return render_template("auth/login.html", form = form)

@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email_entered = form.email.data
    password_entered = form.password.data
    username_entered = form.username.data
    u = User(email = email_entered, username = username_entered, 
        password = password_entered)

    db.session.add(u)
    db.session.commit()
    flash("You can now login.")
    
    # generating token for user
    # token = u.generate_confirmation_token()

    #     # _external = True in Flask Mail tells it to generate an absolute link
    # confirmation_link = url_for('auth.confirm', token = token, _external = True)
    # # send_email(u.email, 'Welcome to Ragtime!', 'mail/welcome', user = u)
    # send_email(u.email, "Confirmation email!", 'auth/confirm', user = u, confirmation_link = confirmation_link)
    # flash("A confirmation email was send to you.")

        # return redirect(url_for('main.index'))
    return render_template('auth/register.html', form = form)





@auth.route('/logout')
def logout():
    logout_user()
    flash("You've been logged out successfully")
    return redirect(url_for('main.index'))

@auth.route('/change_password')
def change_password():
    """ Allows users to change password
    Returns: renders change password form and change-password.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = form.password.data
    new_password = form.new_password.data
    # Checks if old password matches then we can use the new password
    if current_user.verify_password(password) == True:
        current_user.password = new_password
        # add it to the current user and commit
        db.session.add(current_user)
        db.session.commit()
        flash('Password has been changed.')
        # the password change was a success, so user is directed to login
        return redirect(url_for('auth.login'))
    else:
        flash('Old password does not match. Try again.')

    return render_template('auth/change_password.html', form = form)
