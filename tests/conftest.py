import pytest
from app import create_app

# from config import DevConfig   # not needed since tests will only run
# when config is set to DevConfig in app/__init__.py

from app.extensions import db

# if:: from app import create_app ModuleNotFoundError: No module named 'app'
# run pytest as >>> python -m pytest

@pytest.fixture
def app():
    app = create_app('config.TestConfig')    # Explicitly pass the testing config
    
    # Create the tables in the test database
    # DATABASE_URI is set in the config file
    with app.app_context():
        db.create_all()

        yield app

     # Teardown after tests
    with app.app_context():
        db.drop_all()  # Drop tables after tests to clean up


@pytest.fixture
def client(app):
    # app = create_app()
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
