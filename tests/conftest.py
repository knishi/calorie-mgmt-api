import pytest
from webtest import TestApp
from apibase.app import setup_app

@pytest.fixture
def app():
    from oslo_config import cfg
    from oslo_db import options
    from apibase.db import api
    
    # Configure DB for tests
    options.set_defaults(cfg.CONF, connection='sqlite:///:memory:')
    api.setup_db()
    
    return setup_app()

@pytest.fixture
def webapp(app):
    # Valid token by default to keep existing TDD tests Green
    tapp = TestApp(app)
    # webtest mapping: Header 'X-Auth-Token' -> Environ 'HTTP_X_AUTH_TOKEN'
    tapp.extra_environ = {'HTTP_X_AUTH_TOKEN': 'SECRET_TOKEN'}
    return tapp
