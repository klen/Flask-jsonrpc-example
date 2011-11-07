class DefaultConfig(object):
    """ Default configuration for application.
    """
    DEBUG = True
    SECRET_KEY = "secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/api.db"
    SQLALCHEMY_ECHO = False
    MAIL_DEBUG = DEBUG
    DEFAULT_MAIL_SENDER = "support@support.com"
    ACCEPT_LANGUAGES = ['en']


class TestConfig(DefaultConfig):
    """ Configuration for run tests.
    """
    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    SQLALCHEMY_ECHO = False
