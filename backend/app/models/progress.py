
"""
ΜΟΝΤΕΛΟ ΠΡΟΟΔΟΥ
Παρακολουθεί την πρόοδο του μαθητή σε κάθε ενότητα
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class Progress(Base):
    """
    Ο πίνακας progress στη βάση
    Κάθε εγγραφή = πρόοδος ενός μαθητή σε μια ενότητα
    """
    __tablename__ = "progress"
   
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
    is_completed = Column(Boolean, default=False)
    progress_percentage = Column(Float, default=0)
    last_position = Column(Integer, default=0)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
  