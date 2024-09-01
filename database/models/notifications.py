from sqlalchemy import Column, Integer, ForeignKey

from database.models.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    hour = Column(Integer, default=0)
    minute = Column(Integer, default=0)
