from sqlalchemy import Column, DateTime, Float, Integer, String

from .core import Base


class GlucoseLevel(Base):
    __tablename__ = "glucose_levels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    device = Column(String)
    serial_number = Column(String)
    timestamp = Column(DateTime)
    glucose_value = Column(Float)
