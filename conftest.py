import pytest
import dominus.tables

@pytest.fixture(scope='session')
def db_connection_uri():
    return 'postgres://dev:development@localhost:5432/dominus_test'

@pytest.fixture(scope='session')
def tables():
    return dominus.tables

@pytest.fixture()
def user():
    uuid = dominus.platform.create_user('test-user', 'secret')
    return uuid
