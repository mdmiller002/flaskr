"""This module specifies the testing configuration, and provides
some simple test fixtures for pytest to use"""

import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db


# Load in the testing data to populate the database with
with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    """pytest application fixture. This fixture is a sample application set
    to testing mode. This application fixture uses a temporary database, populated
    with dummy data from data.sql"""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """client fixture to emulate a testing client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """runner fixture to emulate a backend runner"""
    return app.test_cli_runner()


class AuthActions(object):
    """AuthActions groups all the related client authentication actions
    into one handy class. These actions are login, logout"""

    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        """Log the client in"""
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        """Log the client out"""
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """auth fixture is an instantiation of the AuthActions class"""
    return AuthActions(client)

