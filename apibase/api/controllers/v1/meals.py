from pecan import expose, rest, request, response
from apibase.common import exception
from apibase.db import api as db_api

class MealsController(rest.RestController):

    @expose(template='json')
    def get_all(self):
        # GET /v1/meals
        # In real case, user_id comes from auth middleware header
        user_id = request.headers.get('X-User-Id', 'admin')
        records = db_api.meal_record_get_all(user_id)
        return [r.to_dict() for r in records]

    @expose(template='json')
    def post(self):
        # POST /v1/meals
        user_id = request.headers.get('X-User-Id', 'admin')
        data = request.json
        
        if 'food_name' not in data or 'calories' not in data:
            raise exception.InvalidInput("Missing food_name or calories")
            
        values = {
            'user_id': user_id,
            'food_name': data['food_name'],
            'calories': data['calories'],
        }
        
        record = db_api.meal_record_create(values)
        response.status = 201
        return record.to_dict()
