import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()

class PhotoStatus(str, enum.Enum):
    PROCESSING = "processing"
    APPROVED = "approved"
    REJECTED = "rejected"
    REPORTED = "reported"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    view_balance = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    nickname = Column(String, nullable=True)

    photos = relationship("Photo", back_populates="owner")
    views = relationship("View", back_populates="viewer")

class Photo(Base):
    __tablename__ = "photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    storage_key = Column(String, nullable=False)
    thumbnail_key = Column(String, nullable=False)
    status = Column(Enum(PhotoStatus), default=PhotoStatus.PROCESSING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="photos")
    views = relationship("View", back_populates="photo")
    reports = relationship("Report", back_populates="photo")

class View(Base):
    __tablename__ = "views"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    viewer_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"), nullable=False)
    liked = Column(Boolean, default=False, nullable=False)
    viewed_at = Column(DateTime, default=datetime.utcnow)

    viewer = relationship("User", back_populates="views")
    photo = relationship("Photo", back_populates="views")

class Report(Base):
    __tablename__ = "reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reporter_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    photo_id = Column(UUID(as_uuid=True), ForeignKey("photos.id"), nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reporter = relationship("User")
    photo = relationship("Photo", back_populates="reports")