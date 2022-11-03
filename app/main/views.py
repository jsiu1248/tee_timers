from . import main
from flask import render_template, session, redirect, url_for, flash, current_app, request, abort, make_response
from .. import db
from flask_login import login_required, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from ..models import User, Role
from ..decorators import permission_required, admin_required

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def for_admins_only():
    return f"Welcome, Administrator! {Permission.ADMIN}"