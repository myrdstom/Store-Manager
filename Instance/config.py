import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.getenv('SECRET')
    DATABASE_URL = 'postgres://wowusxhbqciwzi:7c8533dc3f9c322a373ef785c6a49a399d15da1b4d0df9104667d1ba3fa3b292@ec2-107-21-93-132.compute-1.amazonaws.com:5432/dbml4s1lmr75v5'


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
