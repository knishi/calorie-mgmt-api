from apibase.db import api
from apibase.db import models

def test_create_and_get_item():
    # Setup DB
    from oslo_config import cfg
    from oslo_db import options
    options.set_defaults(cfg.CONF, connection='sqlite:///:memory:')
    api.setup_db()
    
    # Test Create (Red: create_item not implemented)
    item = api.create_item(name="Test CRUD")
    assert item is not None
    assert item.id is not None
    assert item.name == "Test CRUD"

    # Test Get All (Red: get_items not implemented)
    items = api.get_items()
    assert len(items) >= 1
    assert any(i.name == "Test CRUD" for i in items)

    # Test Get One (Red: get_item not implemented)
    fetched = api.get_item(item.id)
    assert fetched is not None
    assert fetched.id == item.id
    assert fetched.name == "Test CRUD"
