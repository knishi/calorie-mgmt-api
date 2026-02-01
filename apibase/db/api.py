from oslo_config import cfg
from oslo_db.sqlalchemy import enginefacade
from apibase.db import models

CONF = cfg.CONF

# Define the engine facade
_context_manager = enginefacade.transaction_context()

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
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.Item).filter_by(id=item_id).first()

def meal_record_create(values):
    try:
        record = models.MealRecord()
        record.update(values)
        with _context_manager.writer.using(_context_manager.writer.get_engine()) as session:
            session.add(record)
            session.flush()
            session.refresh(record)
            return record
    except Exception as e:
        print(f"DEBUG DB ERROR: {e}")
        raise

def meal_record_get_all(user_id):
    with _context_manager.reader.using(_context_manager.reader.get_engine()) as session:
        return session.query(models.MealRecord).filter_by(user_id=user_id).\
            order_by(models.MealRecord.consumed_at.desc()).all()
