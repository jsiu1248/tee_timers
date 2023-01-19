from app import create_app, db, socketio
import os
from app.models import Comment, Role, User, Follow, GolfCourse, Post, City, State
from app.fake import users, post
from flask_migrate import upgrade

# creating create_app instance
app = create_app(os.environ.get("FLASK_CONFIG") or "default")

# adding variables to the shell context so that it doesn't need to be imported again
@app.shell_context_processor
def make_shell_context():
    return dict(db = db, Role = Role, User = User, Comment = Comment, 
    Follow = Follow, Post = Post, City = City, State = State
    )

@app.cli.command()
def deploy():
    """ Run deployment tasks such as upgrading database, inserting roles"""
    # migrate database
    upgrade()

    Role.insert_roles()

    User.add_self_follows()

    GolfCourse.insert_golf_course()

if __name__ == "__golf_app__":
    socketio.run(app, host = "localhost")
