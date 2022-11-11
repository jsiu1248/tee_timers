from sqlalchemy.exc import IntegrityError
from faker import Faker
from . import db
from .models import User
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
                 gender =randint(0,2),
                 age = randint(10,120),
                 day_id = randint(0,6),
                 time_of_day_id = randint(0,1), 
                 ride_or_walk_id = randint(0,1), 
                 handicap_id = randint(0,4), 
                 smoking_id = randint(0,1), 
                 alcohol_id = randint(0,1), 
                 playing_type = randint(0,3) 
                #  , 


                 )
        db.session.add(u)

        # trying to commit data, but if it is a duplicate then it rollbacks
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()
