from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import os
from config import configs
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect

# absolute path
basedir = os.path.abspath(os.path.dirname(__file__))

# instances of classes
db = SQLAlchemy()
bootstrap = Bootstrap()
migrate = Migrate()
mail = Mail()
moment = Moment()
# protects against cross-site request forgery outside of forms
csrf = CSRFProtect()
# login_manager = LoginManager()

# login_manager.login_view = 'auth.login'


def create_app(config_name='default'):
    """ Creating Flask instance and initializing 
    
    """
    # __name__ shortcuts to using the name of the package
    app = Flask(__name__)

    # loading configs before loading extensions
    config_class = configs[config_name]
    app.config.from_object(config_class)

    # initializing app with extensions
    config_class.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    # login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    from .main import main as main_blueprint  # curly braces mean package in vscode
    app.register_blueprint(main_blueprint)

    return app
