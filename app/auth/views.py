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
    return render_template("auth/login.html", form = form)

@auth.route('/register', methods=["GET","POST"])
def register():
    form = RegistrationForm()

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
    return render_template('auth/change_password.html', form = form)
