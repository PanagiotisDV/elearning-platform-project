"""
ΜΟΝΤΕΛΟ ΜΑΘΗΜΑΤΟΣ - ΠΙΝΑΚΑΣ COURSES
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
   

class Course(Base):
    
    __tablename__ = "courses"
      
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    instructor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    instructor = relationship("User", back_populates="courses")
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    enrollments = relationship("Enrollment", back_populates="course") 
    is_published = Column(Boolean, default=False)
    level = Column(String(50), default="beginner")
    #     beginner, intermediate, advanced
    category = Column(String(100), nullable=True)
    #    e.g. "Programming", "Design", "Business"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    