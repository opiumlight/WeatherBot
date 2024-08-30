from sqlalchemy import Column, Integer, DECIMAL, String, Boolean

from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    lat = Column(DECIMAL(precision=8, scale=5), nullable=False)
    lon = Column(DECIMAL(precision=8, scale=5), nullable=False)
    location = Column(String(32), nullable=False)
    notifications = Column(Boolean, default=True)
