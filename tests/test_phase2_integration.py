import json
import datetime
from webtest import TestApp

def test_profile_and_goals_workflow(webapp):
    # 1. Set Profile
    profile_data = {
        'gender': 'male',
        'age': 30,
        'height': 175,
        'weight': 80,
        'activity_level': 1.375
    }
    resp = webapp.post_json('/v1/profile', params=profile_data)
    assert resp.status_int == 201
    assert resp.json['weight'] == 80

    # 2. Set Goal (Target 75kg in 10 days)
    target_date = (datetime.datetime.utcnow() + datetime.timedelta(days=10)).strftime('%Y-%m-%d')
    goal_data = {
        'target_weight': 75,
        'target_date': target_date
    }
    resp = webapp.post_json('/v1/goals', params=goal_data)
    assert resp.status_int == 201
    daily_calories = resp.json['daily_calories']
    assert daily_calories > 0
    print(f"DEBUG: Calculated daily calories: {daily_calories}")

    # 3. Add a meal
    webapp.post_json('/v1/meals', params={'food_name': 'Giant Pizza', 'calories': 1500})

    # 4. Check Summary
    resp = webapp.get('/v1/summary')
    assert resp.status_int == 200
    assert resp.json['total_consumed'] == 1500
    assert resp.json['daily_goal'] == daily_calories
    assert resp.json['remaining'] == daily_calories - 1500
