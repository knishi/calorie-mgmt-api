import webob

import json
from pecan import hooks
from apibase.common import exception
import webob.exc
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

class ErrorHook(hooks.PecanHook):
    def on_error(self, state, exc):
        if isinstance(exc, exception.AppError):
            # Known AppError
            LOG.warning("AppError caught: %s", exc)
            body = json.dumps({'error': {'code': exc.code, 'message': exc.message}}).encode('utf-8')
            return webob.Response(
                body=body,
                status=exc.code,
                content_type='application/json; charset=UTF-8'
            )
        elif isinstance(exc, webob.exc.HTTPError):
            # Already a webob error (e.g. 404 from object dispatch)
            # Ensure we return a JSON body even for webob's default errors
            LOG.warning("HTTPError caught: %s", exc)
            body = json.dumps({'error': {'code': exc.code, 'message': exc.detail or exc.explanation}}).encode('utf-8')
            return webob.Response(
                body=body,
                status=exc.code,
                content_type='application/json; charset=UTF-8'
            )
        else:
            # Unknown exception
            import traceback
            traceback.print_exc()
            LOG.exception("Unhandled exception caught")
            body = json.dumps({'error': {'code': 500, 'message': 'Internal Server Error'}}).encode('utf-8')
            return webob.Response(
                body=body,
                status=500,
                content_type='application/json; charset=UTF-8'
            )
class CorsHook(hooks.PecanHook):
    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, X-Auth-Token'
