
"""
ΜΟΝΤΕΛΟ ΧΡΗΣΤΗ
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class UserRole(str, enum.Enum):
    """Οι ρόλοι του χρήστη"""
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class User(Base):
    """Ο πίνακας users στη βάση"""
    __tablename__ = "users"
    
   
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    role = Column(Enum(UserRole, native_enum=False), default=UserRole.STUDENT)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    
    courses = relationship("Course", back_populates="instructor")

    refresh_tokens = relationship("RefreshToken", back_populates="user")
    
    enrollments = relationship("Enrollment", back_populates="user")
    
    progress = relationship("Progress", back_populates="user")

    quiz_attempts = relationship("QuizAttempt", back_populates="user")
