import webob.dec
import webob.exc

class FakeAuthMiddleware(object):
    """Middleware that mimicks keystonemiddleware behavior."""

    def __init__(self, app):
        self.app = app

    @webob.dec.wsgify
    def __call__(self, req):
        # Handle CORS Preflight (OPTIONS)
        if req.method == 'OPTIONS':
            res = webob.Response()
            res.status = 204
            res.headers['Access-Control-Allow-Origin'] = '*'
            res.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            res.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, X-Auth-Token'
            return res
        
        # Check token
        token = req.headers.get('X-Auth-Token')
        
        if token == 'SECRET_TOKEN':
            req.headers['X-User-Id'] = 'fake_user_id'
            req.headers['X-Project-Id'] = 'fake_project_id'
            req.headers['X-Identity-Status'] = 'Confirmed'
            return req.get_response(self.app)
        
        # Invalid token
        return webob.exc.HTTPUnauthorized("Authentication required")
