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
login_manager = LoginManager()

login_manager.login_view = 'auth.login'


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
    login_manager.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    """registering blue prints"""
    from .main import main as main_blueprint 
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint 
    app.register_blueprint(auth_blueprint)

    from .api import api as api_blueprint 
    app.register_blueprint(api_blueprint)

    if app.config['HTTPS_REDIRECT']:
        from flask_talisman import Talisman
        Talisman(app, content_security_policy={
                'default-src': [
                    "'self'",
                    'cdnjs.cloudflare.com', 'cdn.jsdelivr.net' ,'127.0.0.1:5000' ,'teetimers.herokuapp.com',
                ],
                # allow images from anywhere, 
                #   including unicornify.pictures
                'img-src': '*'
            }
        )

    return app

