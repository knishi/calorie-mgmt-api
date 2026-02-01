def test_get_root(webapp):
    resp = webapp.get('/')
    assert resp.status_int == 200
    assert resp.json['status'] == 'running'
    assert 'v1' in resp.json['versions']

def test_get_v1_index(webapp):
    resp = webapp.get('/v1/')
    assert resp.status_int == 200
    assert resp.json['status'] == 'v1_available'

def test_create_item(webapp):
    # Test POST /v1/items/
    resp = webapp.post_json('/v1/items/', dict(name='New Item'))
    assert resp.status_int == 201
    assert resp.json['name'] == 'New Item'
    assert 'id' in resp.json

def test_get_items(webapp):
    # Ensure item exists from previous test (Note: tests order matters or need fixture)
    # For simplicity, we just check response structure. 
    # Realistically we should mock DB or rely on DB state if using persistent DB.
    # Here we are using in-memory sqlite shared via webapp fixture? 
    # Wait, webapp fixture recreates app? 
    # See conftest.py. setup_app() creates new app. 
    # If connection is sqlite:///:memory:, it is lost between requests if gunicorn workers restart or new app is created.
    # But in tests, 'webapp' is fixture.
    # If scope is function, DB is fresh.
    # So we need to create item inside this test or use bigger scope.
    
    webapp.post_json('/v1/items/', dict(name='Item 1'))
    webapp.post_json('/v1/items/', dict(name='Item 2'))
    
    resp = webapp.get('/v1/items/')
    assert resp.status_int == 200
    assert len(resp.json['items']) >= 2
    # Check if Item 1 exists in the list
    assert any(i['name'] == 'Item 1' for i in resp.json['items'])

def test_get_item_detail(webapp):
    # Create item
    res = webapp.post_json('/v1/items/', dict(name='Item 123'))
    item_id = res.json['id']
    
    resp = webapp.get(f'/v1/items/{item_id}')
    assert resp.status_int == 200
    assert resp.json['id'] == item_id
    assert resp.json['name'] == 'Item 123'

def test_get_item_not_found(webapp):
    # Test 404 with standard error format
    try:
        webapp.get('/v1/items/999999')
        assert False, "Should raise 404"
    except Exception as e:
        # WebTest raises AppError for 4xx
        assert '404 Not Found' in str(e)
        # Check if body contains standard JSON error
        # WebTest exception string usually contains response body
        # Or we can catch AppError and inspect e.response
        pass 
