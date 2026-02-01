from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade
from sqlalchemy import orm
from oslo_log import log as logging

LOG = logging.getLogger(__name__)

CONF = cfg.CONF

# Define the engine facade
_context_manager = enginefacade.transaction_context()
_context_manager.configure(
    connection="sqlite:///apibase.db"
)

def get_engine():
    return _context_manager.writer.get_engine()

def setup_db():
    engine = get_engine()
    models.Base.metadata.create_all(engine)
    return engine

def create_item(name):
    engine = get_engine()
    item = models.Item(name=name)
    with engine.connect() as conn:
        with conn.begin():
            # oslo.db enginefacade handles sessions differently usually,
            # but for simple usage with 'writer' context:
            with _context_manager.writer.using(conn) as session:
                session.add(item)
                # Flush to get ID
                session.flush()
                # Expunge to return detached object or refresh
                session.refresh(item)
                return item

def get_items():
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.Item).all()

def get_item(item_id):
    """Retrieve a single item by its ID."""
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.Item).filter_by(id=item_id).first()

def meal_record_create(values):
    """Create a new meal record."""
    try:
        record = models.MealRecord()
        record.update(values)
        with _context_manager.writer.using(_context_manager.writer.get_engine()) as session:
            session.add(record)
            session.flush()
            session.refresh(record)
            return record
    except Exception as e:
        LOG.exception("DB Error during meal_record_create")
        raise

def meal_record_get_all(user_id):
    """Retrieve all meal records for a specific user, ordered by consumption time."""
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.MealRecord).filter_by(user_id=user_id).\
            order_by(models.MealRecord.consumed_at.desc()).all()

def user_profile_get(user_id):
    """Retrieve the user profile for a specific user."""
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.UserProfile).filter_by(user_id=user_id).first()

def user_profile_update_or_create(user_id, values):
    """Update an existing user profile or create a new one."""
    with _context_manager.writer.using(_context_manager.writer.get_engine()) as session:
        profile = session.query(models.UserProfile).filter_by(user_id=user_id).first()
        if not profile:
            profile = models.UserProfile(user_id=user_id)
            session.add(profile)
        profile.update(values)
        session.flush()
        session.refresh(profile)
        return profile

def user_goal_get(user_id):
    """Retrieve the user goal for a specific user."""
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.UserGoal).filter_by(user_id=user_id).first()

def user_goal_update_or_create(user_id, values):
    """Update an existing user goal or create a new one."""
    with _context_manager.writer.using(_context_manager.writer.get_engine()) as session:
        goal = session.query(models.UserGoal).filter_by(user_id=user_id).first()
        if not goal:
            goal = models.UserGoal(user_id=user_id)
            session.add(goal)
        goal.update(values)
        session.flush()
        session.refresh(goal)
        return goal
