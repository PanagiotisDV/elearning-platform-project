
"""
ΜΟΝΤΕΛΟ ΕΓΓΡΑΦΗΣ
"""

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class EnrollmentStatus(str, enum.Enum):
    """
    Κατάσταση εγγραφής
    """
    ACTIVE = "active"      
    COMPLETED = "completed"  
    DROPPED = "dropped"  

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.ACTIVE)
    progress_percentage = Column(Integer, default=0)
    enrolled_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)