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
    USERS_PER_PAGE = 10
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 25
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


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "data.sqlite")}'

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        import logging
        from logging.handlers import SMTPHandler
        creds = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            creds = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                # logging: to use TLS, must pass tuple (can be empty)
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.MAIL_SENDER,
            toaddrs=[cls.APP_ADMIN],
            subject=cls.MAIL_SUBJECT_PREFIX + " Application Error",
            credentials=creds,
            secure=secure
        )
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

class HerokuConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler
        file_handler.setLevel(file_handler, level=logging.INFO)
        app.logger.addHandler(file_handler)

# giving them all names
configs = {
     'development': DevelopmentConfig,
     'testing': TestingConfig,
     'default': DevelopmentConfig, 
     'production': ProductionConfig, 
     'heroku': HerokuConfig
}
