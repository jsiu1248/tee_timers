import os


basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI =\
         'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'anyRandomLongStringUseNumbersYo#123'
        # Flask-Mail config
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    POSTS_PER_PAGE = 25
    FOLLOWERS_PER_PAGE = 25
    # Other email settings
    # email for the administrator of the flask app
    APP_ADMIN = os.environ.get('APP_ADMIN')

    # this will be the prefix everytime an emails is sent
    MAIL_SUBJECT_PREFIX = 'Tee Timers — '

    # when an email is sent to a user, it is set to this value
    MAIL_SENDER = f'App Admin <{APP_ADMIN}>'
    HTTPS_REDIRECT = False

    # export MAIL_USERNAME=<your Gmail username>
    # remember to change it to your app password
    # export MAIL_PASSWORD=<your Gmail app password>
    # don't include spaces. It didn't like it

    @staticmethod
    def init_app(app):
        pass
configs = {'default': Config}

# getting breakpoints, traces, and reloaders
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_DEV_URL') or \
         'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

# for unit testing
class TestingConfig(Config):
    # making sure that these have names related to testing
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL') or \
'sqlite:///{os.path.join(basedir, "data-test.sqlite")}'



# giving them all names
configs = {
     'development': DevelopmentConfig,
     'testing': TestingConfig,
     'default': DevelopmentConfig 
}
