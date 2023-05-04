from app import create_app, db
import os
from app.models import Comment, Role, User, Follow, GolfCourse, Post, City, State, Day, Gender, TimeOfDay, RideOrWalk, Handicap, Smoking, Drinking, PlayingType
from app.fake import users, post
from flask_migrate import upgrade

# creating create_app instance
app = create_app(os.environ.get("FLASK_CONFIG") or "default")
 
@app.shell_context_processor
def make_shell_context():
    """
    adding variables to the shell context so that it doesn't need to be imported again
    """
    return dict(db = db, Role = Role, User = User, Comment = Comment, 
    Follow = Follow, Post = Post, City = City, State = State
    )

@app.cli.command()
def deploy():
    """ Run deployment tasks such as upgrading database, inserting roles"""
    # migrate database
    upgrade()


    # State.insert_state()
    # City.insert_city()
    # GolfCourse.insert_golf_course()
    # Day.insert_day()
    # Gender.insert_gender()
    # TimeOfDay.insert_timeofday()
    # RideOrWalk.insert_rideorwalk()
    # Handicap.insert_handicap()
    # Smoking.insert_smoking()
    # Drinking.insert_drinking()
    # PlayingType.insert_playingtype()
    # Role.insert_roles()
    # User.add_self_follows()
    # Action.insert_action()
    # Satisfaction.insert_satisfaction()
