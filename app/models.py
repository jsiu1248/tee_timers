from email.policy import default
from . import db # , login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, url_for
# from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime, timedelta
# import jwt
import hashlib
# import bleach
import re
from itsdangerous import Serializer
# from app.exceptions import ValidationError

class Permission:
    FOLLOW = 1
    MODERATE = 2
    ADMIN = 4

class Role(db.Model):
    __tablename__='roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)
    # linking the role model and the user model
    users = db.relationship('User', backref='role', lazy = 'dynamic')
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    # overriding constructor of the Role class
    # so, we can set Permissions to 0, if the permissions were not initially set
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

   
    def __repr__(self):
        """
         returning a string with the name
        """
        return f"<Role {self.name}>"

    @staticmethod
    def insert_roles():
        """
        mapping of role names with their permissions
        """
        roles = {
            'User':             [Permission.FOLLOW],
            'Moderator':        [Permission.FOLLOW,
                                 Permission.MODERATE],
            'Administrator':    [Permission.FOLLOW,
                                 Permission.MODERATE,
                                 Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            # see if role is already in table
            role = Role.query.filter_by(name = r).first()
            if role is None:
                # it's not so make a new one
                role = Role(name = r)
            role.reset_permission()
            # add whichever permissions the role needs
            for perm in roles[r]:
                role.add_permission(perm)
            # if role is the default one, default is True
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()



    def add_permission(self, perm):
        """
        checking if there is a permission and then adding it if there is NOT
        Args: self and perm/permission
        """
        if not self.has_permission(perm):
            self.permissions = self.permissions + perm

    def remove_permission(self, perm):
        """
        checking if there is a permission then substracting if there IS 
        Args: self and perm/permission
        """
        if self.has_permission(perm):
            self.permissions = self.permissions - perm

    def reset_permission(self):
        """
        reset permission by setting to 0
        """
        self.permissions = 0


    def has_permission(self, perm):
        """
            check if role has a particular permission
            if the permission is greater than 0 then it has a particular permission
            Args: self and perm/permission
            Return: the value and if it is true
        """
        return self.permissions & perm == perm


class User(#UserMixin,
 db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    gender = db.Column(db.String(64))
    age = db.Column(db.Integer)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # age = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique = True, index = True)
    confirmed = db.Column(db.Boolean, default = False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    bio = db.Column(db.Text())
    status_id = db.Column(db.Integer)
    frequency_id = db.Column(db.Integer)
    time_of_day_id = db.Column(db.Integer)
    ride_or_walk_id = db.Column(db.Integer)
    handicap_id = db.Column(db.Integer)
    smoking_id = db.Column(db.Integer)
    alcohol_id = db.Column(db.Integer)
    playing_type = db.Column(db.Integer)
    # it will be assigned upon the created of the new User
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # compositions = db.relationship('Composition', backref='artist', lazy='dynamic')
    # following = db.relationship('Follow',
    #                            foreign_keys=[Follow.follower_id],
    #                            backref=db.backref('follower', lazy='joined'),
    #                            lazy='dynamic',
    #                            cascade='all, delete-orphan')
    # followers = db.relationship('Follow',
    #                             foreign_keys=[Follow.following_id],
    #                             backref=db.backref('following', lazy='joined'),
    #                             lazy='dynamic',
    #                             cascade='all, delete-orphan')

    # we want to assign the users their roles right away
    # user constructor
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # assert self.email is not None


    def email_hash(self):
        """
        creating a hash for the email
        Args: self
        Returns: hashed email from lowercased email
        """
        return hashlib.md5(self.email.lower().encode('utf-8')).hexdigest()

    def ping(self):
        """
        When a new request is made, last_seen is updated.
        """
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()