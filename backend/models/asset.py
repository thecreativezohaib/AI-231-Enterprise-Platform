from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from backend.core.database import Base
from datetime import datetime

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, unique=True, index=True)
    type = Column(String, index=True) # e.g., 'DataCenter', 'TelecomTower'
    location = Column(String)
    status = Column(String, default="Active")
    health_score = Column(Float, default=100.0)
    last_updated = Column(DateTime, default=datetime.utcnow)
