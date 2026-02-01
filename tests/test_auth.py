from webtest import AppError
import pytest

def test_auth_enforcement_fail(webapp):
    # This should fail with 401 if auth is enabled
    # We explicitly send BAD token to override the default good one from fixture
    try:
        webapp.get('/v1/items/', headers={'X-Auth-Token': 'BAD_TOKEN'})
        # Note: extra_environ in fixture is fallback, but headers kwarg usually overwrites?
        # If webtest app.extra_environ is set, and we pass headers, they merge. 
        # But 'HTTP_X_AUTH_TOKEN' vs 'X-Auth-Token' might conflict or override.
        # Let's see if passing header overrides environ.
        assert False, "Should have raised AppError(401)"
    except AppError as e:
        assert '401 Unauthorized' in str(e)

def test_auth_enforcement_success(webapp):
    # This should pass if X-Auth-Token is provided
    # Currently implies we need to inject middleware in the fixture or app.py
    # Since we strictly follow TDD, this test will fail because logic isn't there
    resp = webapp.get('/v1/items/', headers={'X-Auth-Token': 'SECRET_TOKEN'})
    assert resp.status_int == 200
