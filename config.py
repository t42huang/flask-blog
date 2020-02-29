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

    SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DB_URL') or \
        'sqlite:///' + os.path.join(basedir, 'database.sqlite')
    

config = {
    'dev': DevConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevConfig
}