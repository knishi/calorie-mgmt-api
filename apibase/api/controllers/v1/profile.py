from pecan import expose, rest, request, response
from apibase.db import api as db_api
from apibase.common import exception

class ProfileController(rest.RestController):

    @expose(template='json')
    def get(self):
        # GET /v1/profile
        user_id = request.headers.get('X-User-Id', 'admin')
        profile = db_api.user_profile_get(user_id)
        if not profile:
            raise exception.ItemNotFound(f"Profile for user {user_id} not found")
        return profile.to_dict()

    @expose(template='json')
    def post(self):
        # POST /v1/profile
        user_id = request.headers.get('X-User-Id', 'admin')
        data = request.json
        profile = db_api.user_profile_update_or_create(user_id, data)
        response.status = 201
        return profile.to_dict()
