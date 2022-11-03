from flask import render_template, session, g, redirect, url_for, flash, current_app, request

# from app.email import send_email
from .forms import LoginForm#, RegistrationForm, ChangePasswordForm # need a period because trying to import within package
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