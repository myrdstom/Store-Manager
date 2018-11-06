import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    DATABASE_URL = 'postgresql://postgres:rasengan1408@localhost:5432/store_manager_pk'


class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True



class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'postgresql://postgres:rasengan1408@localhost:5432/test_store_manager'


class StagingConfig(Config):
    """Configurations for Staging."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
