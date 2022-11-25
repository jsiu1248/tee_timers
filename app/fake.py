from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Post, Comment, UserProfile
from random import randint
import string

def users(count=20):
    """Creating users with fake data
    args: count of how many users needed"""

    # an instance of Faker is called and below are many of their functions with different types of fake data
    fake = Faker()
    i = 0
    while i < count:
        u = User(email = fake.email(),
                 username = fake.user_name(),
                 password = 'password',
                 confirmed = True,
                 name = fake.name()


                 )
        db.session.add(u)

        # trying to commit data, but if it is a duplicate then it rollbacks
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def userprofile(count=20):
    """Creating fake profile data
    args: count of how many users needed"""

    # an instance of Faker is called and below are many of their functions with different types of fake data
    fake = Faker()
    user_count = User.query.count()
    u = User.query.offset(randint(0, user_count - 1)).first()

    i = 0
    while i < count:
        u = UserProfile(
                id  = u.id,
                 city_id = randint(1,100), 
                 state_id = randint(1,20),
                 bio = fake.text(),
                 last_seen=fake.past_date(),
                 gender_id =randint(1,3),
                 age = randint(10,120),
                 day_id = randint(1,7),
                 time_of_day_id = randint(1,2), 
                 ride_or_walk_id = randint(1,2), 
                 handicap_id = randint(1,5), 
                 smoking_id = randint(1,2), 
                 drinking_id = randint(1,2), 
                 playing_type_id = randint(1,5) 
                #  , 


                 )
        db.session.add(u)

        # trying to commit data, but if it is a duplicate then it rollbacks
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()


def post(count=100):
    """Function that creates fake posts
        args: create a certain amount of posts"""
    fake = Faker()

    # checking how many users are in the table
    user_count = User.query.count()
    for i in range(count):
        # offset dicards a certain number of results, n is a random number between 0 and then user_count -1
        # so it is picking a random user and don't care about duplicated users because users can have multiple compositions
        u = User.query.offset(randint(0, user_count - 1)).first()
        p = Post(

        # bs generates cool sounding titles
                        title=string.capwords(fake.bs()),
                        description=fake.text(),
                        timestamp=fake.past_date() ,
                        user_id = u.id,
                        )
        db.session.add(p)
    db.session.commit()
    for p in Post.query.all():
        p.generate_slug()

