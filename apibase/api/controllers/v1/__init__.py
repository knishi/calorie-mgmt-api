from pecan import expose, rest

from pecan import expose, rest, request, response
from oslo_log import log as logging
from apibase.db import api as db_api
from apibase.common import exception
from apibase.api.controllers.v1 import meals as meals_controller
from apibase.api.controllers.v1 import profile as profile_controller
from apibase.api.controllers.v1 import goals as goals_controller
from apibase.api.controllers.v1 import summary as summary_controller

LOG = logging.getLogger(__name__)

class ItemsController(rest.RestController):
    @expose(template='json')
    def get_one(self, item_id):
        # GET /v1/items/{item_id}
        LOG.info("Attributes: item_id=%s", item_id)
        item = db_api.get_item(item_id)
        if not item:
            LOG.warning("Item not found: %s", item_id)
            raise exception.ItemNotFound(f"Item {item_id} not found")
        return dict(id=item.id, name=item.name)

    @expose(template='json')
    def get_all(self):
        # GET /v1/items
        LOG.info("Listing all items")
        items = db_api.get_items()
        return dict(items=[dict(id=i.id, name=i.name) for i in items])
        
    @expose(template='json')
    def post(self):
        # POST /v1/items/
        data = request.json
        if not data or 'name' not in data:
            LOG.error("Invalid input for creation")
            raise exception.InvalidInput("Name is required")
            
        LOG.info("Creating item: %s", data['name'])
        item = db_api.create_item(name=data['name'])
        response.status = 201
        return dict(id=item.id, name=item.name)

class V1Controller(object):
    @expose(template='json')
    def index(self):
        return dict(status='v1_available')
    
    # Sub-controller for /v1/items
    items = ItemsController()

    # Sub-controller for /v1/meals
    meals = meals_controller.MealsController()

    # Sub-controller for /v1/profile
    profile = profile_controller.ProfileController()

    # Sub-controller for /v1/goals
    goals = goals_controller.GoalsController()

    # Sub-controller for /v1/summary
    summary = summary_controller.SummaryController()
