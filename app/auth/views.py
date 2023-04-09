import email
from flask import render_template, session, g, redirect, url_for, flash, current_app, request

from app.email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm # need a period because trying to import within package
# from app.main.forms import EditProfileForm
from .. import db
from ..models import User, Role, UserProfile, Img
from flask_login import login_required, logout_user, login_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from . import auth
from PIL import Image
from io import BytesIO

@auth.route('/login' , methods=["GET", "POST"])
def login():
    """ 
    Allows users to login
    """
    # form is created
    form = LoginForm()

    email_entered = form.email.data
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
    flash("The username/password is invalid")


    return render_template("auth/login.html", form = form)

@auth.route('/register', methods=["GET","POST"])
def register():
    """ 
    Allows users to register an account
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        email_entered = form.email.data
        password_entered = form.password.data
        username_entered = form.username.data
        u = User(email = email_entered, username = username_entered, 
        password = password_entered)

        try:
            db.session.add(u)
            db.session.commit()
        except:
            flash('Error occurred while creating account. Please try again later.', 'error')
            return redirect(url_for('auth.register'))
        
        try:
            p = User.query.filter_by(username = username_entered).first()

            picture = Img(id = p.id, img = "istockphoto-515229864-612x612.jpeg")

            #testing to see if the relative path isn't needed. 
            #picture = Img(id = p.id, img = "../static/jpeg/users/istockphoto-515229864-612x612.jpeg")

            db.session.add(picture)
            db.session.commit()
        
        except:
            db.session.rollback()
            flash('Error occurred while uploading image. Please try again later.', 'error')
            return redirect(url_for('auth.register'))

        try:    
            p = User.query.filter_by(username = username_entered).first()

            up = UserProfile(id = p.id, profile_picture_id = p.id )

            db.session.add(up)
            db.session.commit()
        
        except:
            db.session.rollback()
            flash('Error occurred while creating profile. Please try again later.', 'error')
            return redirect(url_for('auth.register'))

        flash("You can now login.")
    
    # generating token for user
        token = u.generate_confirmation_token()

    #     # _external = True in Flask Mail tells it to generate an absolute link
        confirmation_link = url_for('auth.confirm', token = token, _external = True)
        # send_email(u.email, 'Welcome to Tee Timers!', 'mail/welcome', user = u)
        send_email(u.email, "Confirmation email!", 'auth/confirm', user = u, confirmation_link = confirmation_link)
        flash("A confirmation email was send to you.")

        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form = form)





@auth.route('/logout')
def logout():
    """ 
    Allows users to logout
    """
    logout_user()
    flash("You've been logged out successfully")
    return redirect(url_for('main.index'))

@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    """ Allows users to change password
    Returns: renders change password form and change-password.
    """
    form = ChangePasswordForm()
    if form.validate_on_submit():
        password = form.old_password.data
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


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """"
    Confirm the user's email by taking a token and attempting to confirm the user. We want to confirm the current_user
    because we don't want an old user.

    Args: token(str): Generated after registering email. Token is in confirmation link sent to user's email.
    Returns: Redirect to index page.

    """
    if current_user.confirmed:
        flash("You're already confirmed, silly!")
        return redirect(url_for('main.index'))
    
    # if the token is confirmed then the user is commited 
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account! Thank you.')
    else:
        flash("Whoops! That confirmation link either expired, or it isn't valid.")
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    """
    This happens before app request and any other view function. 
    You can rescrict a user's access to the app for users that are not confirmed.
    Returns: unconfirmed page if user is unconfirmed
    """
    # back slash means line continuation
    # they must be signed in and not confirmed and the endpoint is in the auth blueprint
    if current_user.is_authenticated:
        # ping is called everytime a request is made
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint \
                and request.blueprint != 'auth' \
                and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))



@auth.route('/unconfirmed')
def unconfirmed():
    """
    Landing page for the unconfirmed. Telling them that they still need to confirm.

    Returns: auth/unconfirmed.html
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    # returning unconfirmed template
    return render_template('auth/unconfirmed.html', user = current_user)

@auth.route('/resend_confirmation')
def resend_confirmation():
    """
    Function that resends confirmation link to the user's email

    Returns: Redirects to the auth/unconfirmed page
    """

    # u is the user before, but now Flask tracks it with current_user
    user = current_user

    token = user.generate_confirmation_token()

    # url_for helps create dynamic links
    # _external = True in Flask Mail tells it to generate an absolute link
    confirmation_link = url_for('auth.confirm', token = token, _external = True)
    send_email(user.email, "Confirmation Email!", 'auth/confirm', user=user, confirmation_link = confirmation_link)
    flash("Check your email for the reconfirmation email.")
    return redirect(url_for('auth.unconfirmed'))
