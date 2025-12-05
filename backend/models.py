from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Video(Base):
    __tablename__ = "videos"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    channel_id = Column(String, nullable=False, index=True)
    channel_name = Column(String, nullable=False)
    published = Column(DateTime, nullable=False, index=True)
    url = Column(String, nullable=False)
    embed_url = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    is_live = Column(Boolean, default=False, index=True)
    duration = Column(String)
    view_count = Column(Integer)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Channel(Base):
    __tablename__ = "channels"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    rss_url = Column(String, nullable=False)
    thumbnail = Column(String)
    subscriber_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Category(Base):
    __tablename__ = "categories"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    color = Column(String, nullable=False)
    channels = Column(Text)  # Comma-separated channel IDs
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
