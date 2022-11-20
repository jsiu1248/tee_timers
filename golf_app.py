from app import create_app, db
import os
from app.models import Comment, Role, User, Follow, Location, GolfCourse, Post
from app.fake import users, comment
from flask_migrate import upgrade

# creating create_app instance
app = create_app(os.environ.get("FLASK_CONFIG") or "default")

# adding variables to the shell context so that it doesn't need to be imported again
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, Role = Role, User = User, Comment = Comment, Follow = Follow, Post = Post)

@app.cli.command()
def deploy():
    """ Run deployment tasks such as upgrading database, inserting roles"""
    # migrate database
    upgrade()

    Role.insert_roles()

    User.add_self_follows()

    Location.insert_location()

    GolfCourse.insert_golf_course()
