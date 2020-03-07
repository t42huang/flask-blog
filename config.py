import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # add in a secret key for this app to avoid CSRF (Cross-Site Request Forgery) on forms
    SECRET_KEY = os.environ.get('FB_SECRET_KEY')

    ## Mail configs
    MAIL_SERVER = os.environ.get('MAIL_SERVER')

    # MAIL_PORT = 587
    # MAIL_PORT = 465
    MAIL_PORT = 25
    
    MAIL_USE_TLS = True
    # MAIL_USE_SSL = True # this is needed for 465    
    
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FB_MAIL_SUBJECT_PREFIX = '[Flask Blog]'
    FB_MAIL_SENDER = os.environ.get('FLASKBLOG_SENDER')
    FLASKBLOG_ADMIN = os.environ.get('FLASKBLOG_ADMIN')

    FBLOG_POSTS_PER_PAGE = 3 # 20
    FBLOG_COMMENTS_PER_PAGE = 3

    SSL_REDIRECT = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    FBLOG_SLOW_DB_QUERY_TIME = 0.5    

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database-dev.sqlite')
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database-testing.sqlite')
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # email errors to the administrators
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls, 'MAIL_USERNAME', None) is not None:
            credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
            if getattr(cls, 'MAIL_USE_TLS', None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
            fromaddr=cls.FB_MAIL_SENDER,
            toaddrs=[cls.FLASKBLOG_ADMIN],
            subject=cls.FB_MAIL_SUBJECT_PREFIX + ' Application Error',
            credentials=credentials,
            secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False

    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)

        # handle reverse proxy server headers
        from werkzeug.contrib.fixers import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


class DockerConfig(ProductionConfig):
    @classmethod
    def init_app(cls, app):
        ProductionConfig.init_app(app)
        
        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'heroku': HerokuConfig,
    'docker': DockerConfig,

    'default': DevConfig
}