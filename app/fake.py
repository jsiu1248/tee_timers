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
        u = User(email=fake.email(),
                 username=fake.user_name(),
                 password='password',
                 confirmed=True,
                 name=fake.name(),
                 city=fake.city(),
                 state=fake.state(),
                 bio=fake.text(),
                 last_seen=fake.past_date()
                #  gender =fake.,
                #  age =, 
                #  bio =, 
                #  status_id = , 
                #  frequency_id =,
                #  time_of_day_id = , 
                #  ride_or_walk_id = , 
                #  handicap_id, 
                #  smoking_id, 
                #  alcohol_id , 
                #  playing_type = 
                #  , 

                 )
        db.session.add(u)

        # trying to commit data, but if it is a duplicate then it rollbacks
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()