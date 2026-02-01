from pecan import expose, rest, request
import datetime
from apibase.db import api as db_api

class SummaryController(rest.RestController):

    @expose(template='json')
    def get(self):
        # GET /v1/summary
        user_id = request.headers.get('X-User-Id', 'admin')
        
        # Today's consumed
        records = db_api.meal_record_get_all(user_id)
        today = datetime.datetime.utcnow().date()
        
        today_records = [r for r in records if r.consumed_at.date() == today]
        total_consumed = sum(r.calories for r in today_records)
        
        # Goal
        goal_record = db_api.user_goal_get(user_id)
        daily_goal = goal_record.daily_calories if goal_record else 2000
        
        remaining = daily_goal - total_consumed
        
        return {
            'date': today.isoformat(),
            'total_consumed': total_consumed,
            'daily_goal': daily_goal,
            'remaining': remaining,
            'status': 'under_limit' if remaining >= 0 else 'over_limit'
        }
