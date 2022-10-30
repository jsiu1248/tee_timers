from app import create_app, db
import os

from flask_migrate import upgrade

# creating create_app instance
app = create_app(os.environ.get("FLASK_CONFIG") or "default")

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)
