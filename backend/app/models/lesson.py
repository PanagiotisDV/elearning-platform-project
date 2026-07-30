# backend/app/models/lesson.py
"""
ΜΟΝΤΕΛΟ ΕΝΟΤΗΤΑΣ
"""


from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base



class Lesson(Base):
    """
    Μια ενότητα μέσα σε ένα μάθημα
    """
    __tablename__ = "lessons"
  
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    course = relationship("Course", back_populates="lessons")
    content_type = Column(String(50), default="video")
    content_url = Column(String(500), nullable=True)
    content_text = Column(Text, nullable=True)
    order = Column(Integer, default=0)
    duration_minutes = Column(Float, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    quizzes = relationship("Quiz", back_populates="lesson", cascade="all, delete-orphan")
    progress = relationship("Progress", back_populates="lesson")
   