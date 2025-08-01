from database import Base
from sqlalchemy import JSON, Column, Integer, String, Text
from sqlalchemy.orm import relationship


class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    emoji_icon = Column(String, nullable=True, default="")  # e.g., "🎮"
    activity_type = Column(
        String, nullable=False
    )  # e.g., 'choice-story', 'unlimited', etc.
    activity_settings = Column(
        JSON, default={}
    )  # extra config per activity (activity-specific settings)

    sessions = relationship("Session", back_populates="activity")
