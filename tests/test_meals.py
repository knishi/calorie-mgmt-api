from webtest import TestApp
import json

def test_create_meal_record(webapp):
    params = {
        'food_name': 'Apple',
        'calories': 95
    }
    response = webapp.post_json('/v1/meals', params=params)
    assert response.status_int == 201
    assert response.json['food_name'] == 'Apple'
    assert response.json['calories'] == 95
    assert 'id' in response.json
    assert 'consumed_at' in response.json

def test_get_meal_records(webapp):
    # Setup: Create a record first
    webapp.post_json('/v1/meals', params={'food_name': 'Banana', 'calories': 105})
    
    response = webapp.get('/v1/meals')
    assert response.status_int == 200
    assert len(response.json) >= 1
    # Should be the latest one (Banana)
    assert response.json[0]['food_name'] == 'Banana'

def test_create_meal_invalid_data(webapp):
    # Missing calories
    params = {'food_name': 'Mystery Food'}
    response = webapp.post_json('/v1/meals', params=params, expect_errors=True)
    assert response.status_int == 400
