import webob.dec
import webob.exc

class FakeAuthMiddleware(object):
    """Middleware that mimicks keystonemiddleware behavior."""

    def __init__(self, app):
        self.app = app

    @webob.dec.wsgify
    def __call__(self, req):
        # Allow OPTIONS for CORS preflight (if needed) or healthcheck
        if req.method == 'OPTIONS':
            return req.get_response(self.app)
        
        # Check token
        token = req.headers.get('X-Auth-Token')
        
        if token == 'SECRET_TOKEN':
            req.headers['X-User-Id'] = 'fake_user_id'
            req.headers['X-Project-Id'] = 'fake_project_id'
            req.headers['X-Identity-Status'] = 'Confirmed'
            return req.get_response(self.app)
        
        # Invalid token
        return webob.exc.HTTPUnauthorized("Authentication required")
