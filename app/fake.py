from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User, Comment
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
                 name = fake.name(),
                 city = fake.city(),
                 state = fake.state(),
                 bio = fake.text(),
                 last_seen=fake.past_date(),
                 gender =randint(1,3),
                 age = randint(10,120),
                 day_id = randint(1,7),
                 time_of_day_id = randint(1,2), 
                 ride_or_walk_id = randint(1,2), 
                 handicap_id = randint(1,5), 
                 smoking_id = randint(1,2), 
                 alcohol_id = randint(1,2), 
                 playing_type = randint(1,5) 
                #  , 


                 )
        db.session.add(u)

        # trying to commit data, but if it is a duplicate then it rollbacks
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def comment(count=100):
    """Function that creates fake comments
        args: create a certain amount of comments"""
    fake = Faker()

    # checking how many users are in the table
    user_count = User.query.count()
    for i in range(count):
        # offset dicards a certain number of results, n is a random number between 0 and then user_count -1
        # so it is picking a random user and don't care about duplicated users because users can have multiple compositions
        u = User.query.offset(randint(0, user_count - 1)).first()
        c = Comment(

        # bs generates cool sounding titles
                        title=string.capwords(fake.bs()),
                        comment=fake.text(),
                        timestamp=fake.past_date() ,
                        user_id=randint(1, user_count)
                        )
        db.session.add(c)
    db.session.commit()
    for c in Comment.query.all():
        c.generate_slug()

