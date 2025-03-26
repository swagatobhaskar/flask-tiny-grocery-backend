from os import path, environ
from dotenv import load_dotenv

BASEDIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASEDIR, ".env"))

class Config:
    """Base config."""
    DEBUG = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
class DevConfig(Config):
    DEBUG = True
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'dev_grocery_inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'test_grocery_inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    DEBUG = False
    TESTING = False
    # SECRET_KEY is set by kubernetes secret in production
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URI')
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'dev_grocery_inventory.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
