from pecan import expose, rest, request, response
import datetime
from apibase.db import api as db_api
from apibase.common import utils
from apibase.common import exception

class GoalsController(rest.RestController):

    @expose(template='json')
    def get(self):
        # GET /v1/goals
        user_id = request.headers.get('X-User-Id', 'admin')
        goal = db_api.user_goal_get(user_id)
        if not goal:
            raise exception.ItemNotFound(f"Goal for user {user_id} not found")
        return goal.to_dict()

    @expose(template='json')
    def post(self):
        # POST /v1/goals
        user_id = request.headers.get('X-User-Id', 'admin')
        data = request.json
        
        target_weight = data.get('target_weight')
        target_date_str = data.get('target_date')
        
        if not target_weight or not target_date_str:
            raise exception.InvalidInput("target_weight and target_date are required")
            
        target_date = datetime.datetime.strptime(target_date_str, '%Y-%m-%d')
        
        # Calculate daily calories
        profile = db_api.user_profile_get(user_id)
        if not profile:
             raise exception.InvalidInput("Please set your profile first")
             
        daily_calories = utils.calculate_daily_goal(profile, target_weight, target_date)
        
        values = {
            'target_weight': target_weight,
            'target_date': target_date,
            'daily_calories': daily_calories
        }
        
        goal = db_api.user_goal_update_or_create(user_id, values)
        response.status = 201
        return goal.to_dict()
