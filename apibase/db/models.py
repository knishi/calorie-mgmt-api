import datetime
from oslo_db.sqlalchemy import models
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

class _Base(models.ModelBase):
    def to_dict(self):
        """Simple model to dict conversion."""
        res = {}
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            if isinstance(value, datetime.datetime):
                value = value.isoformat()
            res[column.name] = value
        return res

Base = declarative_base(cls=_Base)

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class MealRecord(Base):
    __tablename__ = 'meal_records'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(255), nullable=False, index=True)
    food_name = Column(String(255), nullable=False)
    calories = Column(Integer, nullable=False)
    consumed_at = Column(DateTime, default=datetime.datetime.utcnow)
class UserProfile(Base):
    __tablename__ = 'user_profiles'

    user_id = Column(String(255), primary_key=True)
    gender = Column(String(10), nullable=True)  # male/female
    age = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)  # cm
    weight = Column(Integer, nullable=True)  # kg
    activity_level = Column(Float, default=1.2)  # 1.2 to 1.9

class UserGoal(Base):
    __tablename__ = 'user_goals'

    user_id = Column(String(255), primary_key=True)
    target_weight = Column(Integer, nullable=True)
    target_date = Column(DateTime, nullable=True)
    daily_calories = Column(Integer, nullable=False)
