"""
ΜΟΝΤΕΛΑ ΓΙΑ QUIZZES (ΤΕΣΤ)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON, Boolean, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

# ========================================
# 1. QUIZ MODEL
# ========================================
class Quiz(Base):
    """
    Ένα τεστ που ανήκει σε μια ενότητα
    """
    __tablename__ = "quizzes"
    
    # 1.1. ΒΑΣΙΚΑ
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    lesson = relationship("Lesson", back_populates="quizzes")
    time_limit_minutes = Column(Integer, default=0)
    passing_score = Column(Integer, default=70)
    max_attempts = Column(Integer, default=3)
    is_published = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    questions = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
    attempts = relationship("QuizAttempt", back_populates="quiz")
   

# ========================================
# 2. QUESTION MODEL
# ========================================
class Question(Base):
    """
    Μια ερώτηση σε ένα quiz
    """
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    quiz = relationship("Quiz", back_populates="questions")
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), default="multiple_choice")
    options = Column(JSON, nullable=True)
    #  Οι επιλογές (π.χ. ["A", "B", "C", "D"])
    correct_answer = Column(Text, nullable=False)
    points = Column(Integer, default=1)
    order = Column(Integer, default=0)
 
# ========================================
# 3. QUIZ ATTEMPT MODEL
# ========================================
class QuizAttempt(Base):
    """
    Μια προσπάθεια ενός χρήστη σε ένα quiz
    """
    __tablename__ = "quiz_attempts"
    
    
    id = Column(Integer, primary_key=True, index=True)
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=0)
    percentage = Column(Integer, default=0)
    is_passed = Column(Boolean, default=False)
    answers = Column(JSON, nullable=True)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)