from email.policy import default
from . import db , login_manager
from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app, url_for
from flask_login import UserMixin, AnonymousUserMixin
from datetime import datetime, timedelta
import jwt
import hashlib
import bleach
import re
from itsdangerous import Serializer
from app.exceptions import ValidationError
import json

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


class Follow(db.Model):
    __tablename__ = 'follows'

    # ID of the user who follows another
    follower_id = db.Column(db.Integer,
                            db.ForeignKey('users.id'),
    # with both columns as primary key then both foreign keys form the primary key
                            primary_key=True)
    
    # ID of the user who is being followed
    following_id = db.Column(db.Integer,
                             db.ForeignKey('users.id'),
                             primary_key=True)
    # time the user started following
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__='users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    # age = db.Column(db.Integer)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique = True, index = True)
    confirmed = db.Column(db.Boolean, default = False)
    name = db.Column(db.String(64))
    comment = db.relationship('Comment', backref='users', lazy='dynamic')
    user_profile = db.relationship('UserProfile', backref='users', lazy='dynamic')

    post = db.relationship('Post', backref='users', lazy='dynamic')

    following = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.following_id],
                                backref=db.backref('following', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')

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

    @property
    def password(self):
        """
        errors out when someone tries to read it
        Args: self
        Return: attribute error
        """
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        """
        allow the user to still write a password
        flask already has a function that helps with hashing and adding salt
        Args: self, password
        """
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        """
        it takes the password and hash together and returns true if correct
        Args: self and password
        Return True or False
        """
        return check_password_hash(self.password_hash, password)

    def can(self, perm):
        """
        check if user can do something
        Args: self and perm/permission
        Return: Boolean
        """
        return self.role is not None and self.role.has_permission(perm)


    def is_administrator(self):
        """
        check if the user is an admin
        Return: Boolean
        """
        return self.can(Permission.ADMIN)

    def generate_confirmation_token(self, expiration_sec=3600):
        """
        generates a token
        Args: self and expiration time 
        Return: token
        """
        # For jwt.encode(), expiration is provided as a time in UTC
        # It is set through the "exp" key in the data to be tokenized
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_sec)
        data = {"exp": expiration_time, "confirm_id": self.id}
        # Use SHA-512 (known as HS512) for the hash algorithm
        token = jwt.encode(data, current_app.secret_key, algorithm="HS512")
        return token

    def confirm(self, token):
        """
        checks whether token is valid or not for user and have to make sure that they are logged in
        Args: self and token
        Return: Boolean
        """
        try:
            # Ensure token valid and hasn't expired
            data = jwt.decode(token, current_app.secret_key, algorithms=["HS512"])
        except jwt.ExpiredSignatureError as e:
            # token expired
            return False
        except jwt.InvalidSignatureError as e:
            # key does not match
            return False
        # The token's data must match the user's ID
        if data.get("confirm_id") != self.id:
            return False
        # All checks pass, confirm the user
        self.confirmed = True
        db.session.add(self)
        # the data isn't committed yet as you want to make sure the user is currently logged in.
        return True

    def follow(self, user):
        """
        follows user. A new row is inserted in the follows table linking it to the user passed in
        Args: user that you want to follow
        """
        if not self.is_following(user):
            f = Follow(follower=self, following=user)
            db.session.add(f)

    def unfollow(self, user):
        """unfollows user. A row is deleted in the follows table linking the user  passed in 
        Args: user that you want to unfollow
        """
        f = self.following.filter_by(following_id=user.id).first()
        if f:
            db.session.delete(f)

    def is_following(self, user):
        """ determines if you are following user
        Args: user that you want to see if you are following
        """
        if user.id is None:
            return False
        return self.following.filter_by(
            following_id=user.id).first() is not None

    def is_a_follower(self, user):
        """ determines if another user is a follower
        Args: user is or is not a follower
        """
        if user.id is None:
            return False
        return self.followers.filter_by(
            follower_id=user.id).first() is not None

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                db.session.add(user)
                db.session.commit()



class AnonymousUser(AnonymousUserMixin):
    # checking that a user has a given permission and can perform a task
    def can(self, perm):
        return False
    def is_administrator(self):
        return False

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description_html = db.Column(db.Text)
    slug = db.Column(db.String(128), unique=True)
    

    @staticmethod
    def on_changed_description(target, value, oldvalue, initiator):
        """
        "listener" of SQLAlchemy's "set" event for description. the function will be called whenever the
        description changes.
        """
        allowed_tags = ['a']
        # clean is called, takes a list of allowed tags
        # linkify will make hyperlinks out of urls in text. <a> tags are created automatically 
        html = bleach.linkify(bleach.clean(value,
        # allowed tags is a whitelist
                                           tags=allowed_tags,
        # strip away any extra characters
                                           strip=True))
        target.description_html = html

    def generate_slug(self):
        """
        The slug is long enough for any title. REGEX is used to make it more readable and lowered.
        The id is added to make sure that it is unique. 
        """
        self.slug = f"{self.id}-" + re.sub(r'[^\w]+', '-', self.title.lower())
        db.session.add(self)
        db.session.commit()



db.event.listen(Post.description,
                'set',
                Post.on_changed_description)

# have to let login_manager know about the new class through the anonymous_user attribute
# why does this need to be done again? Since in the definition is already named AnonymousUser
login_manager.anonymous_user = AnonymousUser

# login manager needs help with getting users
# LoginManager will call load_user() to find out info about users
# takes an id and returns the user
# https://stackoverflow.com/questions/26606391/flask-login-attributeerror-user-object-has-no-attribute-is-active
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def __repr__(self):
    return f"<User {self.username}>"

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    description_html = db.Column(db.Text)
    slug = db.Column(db.String(128), unique=True)

# class GenderLookup:
#     """
#     Gender Lookup
#     """
#     # MALE = 1
#     # FEMALE = 2
#     # OTHER = 3

# class Day:
#     """
#     Day Lookup
#     """
#     MONDAY = 1
#     TUESDAY = 2
#     WEDNESDAY = 3
#     THURSDAY = 4
#     FRIDAY = 5
#     SATURDAY = 6
#     SUNDAY = 7

# class TimeOfDay:
#     """
#     Time of Day Lookup
#     """
#     MORNING = 1
#     AFTERNOON = 2

# class RideOrWalk:
#     """
#     Ride or Walk Lookup
#     """
#     RIDE = 1
#     WALK = 2

# class Handicap:
#     """
#     Handicap Lookup
#     """
#     TWENTY = 1
#     FIFTEEN = 2
#     TEN = 3
#     FIVE = 4

# class Smoking:
#     """Smoking Lookup"""
#     NO = 1
#     YES = 2

# class Drinking:
#     """Drinking Lookup"""
#     NO = 1
#     YES = 2

# class PlayingType:
#     """Playing Type Lookup"""
#     LEISURE = 1
#     BETTING = 2
#     COMPETITIVE = 3
#     DRIVINGRANGE = 4
#     LEARNING = 5

class UserProfile(db.Model):
    """
    User Profile information. 
    """
    id = db.Column(db.Integer, primary_key = True)
    gender_id = db.Column(db.Integer)
    age = db.Column(db.Integer)
    city_id = db.Column(db.Integer)
    state_id = db.Column(db.Integer)
    bio = db.Column(db.Text())
    day_id = db.Column(db.Integer)
    time_of_day_id = db.Column(db.Integer)
    ride_or_walk_id = db.Column(db.Integer)
    handicap_id = db.Column(db.Integer)
    smoking_id = db.Column(db.Integer)
    drinking_id = db.Column(db.Integer)
    playing_type_id = db.Column(db.Integer)
    # it will be assigned upon the created of the new User
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

class Gender(db.Model):
    __tablename__ = 'gender'
    id = db.Column(db.Integer, primary_key = True)
    gender = db.Column(db.String(64))

class Day(db.Model):
    __tablename__ = 'day'
    id = db.Column(db.Integer , primary_key = True)
    day = db.Column(db.String(64))

    @staticmethod
    def insert_day():
        "adding day lookup to database"
        # load data in json
        data = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
        "Saturday", "Sunday"]
        for day in data:
                day = Day(day = day)
                db.session.add(day)
        db.session.commit()


class TimeOfDay(db.Model):
    __tablename__ = 'time_of_day'
    id = db.Column(db.Integer, primary_key = True)
    time_of_day = db.Column(db.String(64))

class RideOrWalk(db.Model):
    __tablename__ = 'ride_or_walk'
    id = db.Column(db.Integer, primary_key = True)
    ride_or_walk = db.Column(db.String(64))

class Handicap(db.Model):
    __tablename__ = 'handicap'
    id = db.Column(db.Integer, primary_key = True)
    handicap = db.Column(db.String(64))

class Smoking(db.Model):
    __tablename__ = 'smoking'
    id = db.Column(db.Integer, primary_key = True)
    smoking = db.Column(db.String(64))

class Drinking(db.Model):
    __tablename__ = 'drinking'
    id = db.Column(db.Integer, primary_key = True)
    drinking = db.Column(db.String(64))

class PlayingType(db.Model):
    __tablename__ = 'playing_type'
    id = db.Column(db.Integer, primary_key = True)
    playing_type = db.Column(db.String(64))







class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer)
    city_id = db.Column(db.String(64), primary_key=True)
    city = db.Column(db.String(64))

    @staticmethod
    def insert_city():
        "adding city and state data from json file."
        # load data in json
        with open('app/static/us-cities-demographics.json', 'r') as loc:
            data = json.load(loc)
        for dicts in data:
            city = dicts['recordid']
            if not City.query.filter_by(city_id = city).first():
                city_id = dicts['recordid']
                city = dicts['fields']['city']
                city = City(city_id = city_id, city = city)
                db.session.add(city)
            else:
                pass
        db.session.commit()

class State(db.Model):
    __tablename__ = 'state'
    id = db.Column(db.Integer)
    state_id = db.Column(db.String(64), primary_key=True)
    state = db.Column(db.String(64))

    @staticmethod
    def insert_state():
        "adding city and state data from json file."
        # load data in json
        with open('app/static/us-cities-demographics.json', 'r') as loc:
            data = json.load(loc)
        for dicts in data:
            state = dicts['recordid']
            if not State.query.filter_by(state_id = state).first():
                state_id = dicts['recordid']
                state = dicts['fields']['state']
                state = State(state_id = state_id, state = state)
                db.session.add(state)
            else:
                pass
        db.session.commit()


class GolfCourse(db.Model):
    __tablename__ = 'golfcourse'
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    course = db.Column(db.String(64))

    def insert_golf_course():
        "adding city and state data from json file."
        # load data in json
        with open('app/static/California_Golf_Courses.json', 'r') as loc:
            data = json.load(loc)
        for dicts in data:
                city = dicts['City']
                state = dicts['State']
                course = dicts['Club']
                golf_course = GolfCourse(city = city, state = state, 
                course = course)
                db.session.add(golf_course)
        db.session.commit()

        # figure out how to auto insert data later
        # State.insert_state()
        # City.insert_city()
        # GolfCourse.insert_golf_course()