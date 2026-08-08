"""
QUIZ ENDPOINTS
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.lesson import Lesson
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.course import Course
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.user import User
from app.schemas.quiz import (
    QuizCreate, QuizUpdate, QuizResponse, QuizDetailResponse,
    QuestionCreate, QuestionResponse, QuizSubmit, QuizAttemptResponse
)
from app.api.deps import get_current_active_user, require_role
from datetime import datetime, timezone
import json

router = APIRouter()

# ========================================
# 1. CREATE QUIZ (INSTRUCTOR)
# ========================================
@router.post("/lessons/{lesson_id}/quizzes", response_model=QuizResponse, status_code=status.HTTP_201_CREATED)
async def create_quiz(
    lesson_id: int,
    quiz_data: QuizCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΔΗΜΙΟΥΡΓΙΑ ΝΕΟΥ QUIZ ΣΕ ΜΙΑ ΕΝΟΤΗΤΑ
    """

    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    

    result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = result.scalar_one_or_none()
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only create quizzes in your own courses"
        )
    

    new_quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        lesson_id=lesson_id,
        time_limit_minutes=quiz_data.time_limit_minutes,
        passing_score=quiz_data.passing_score,
        max_attempts=quiz_data.max_attempts,
        is_published=quiz_data.is_published
    )
    
    db.add(new_quiz)
    await db.flush()  # Παίρνουμε το ID
    

    for q_data in quiz_data.questions:
        question = Question(
            quiz_id=new_quiz.id,
            question_text=q_data.question_text,
            question_type=q_data.question_type,
            options=q_data.options,
            correct_answer=q_data.correct_answer,
            points=q_data.points,
            order=q_data.order
        )
        db.add(question)
    
    await db.commit()
    await db.refresh(new_quiz)
    
    return new_quiz

# ========================================
# 2. GET QUIZZES BY LESSON
# ========================================
@router.get("/lessons/{lesson_id}/quizzes", response_model=List[QuizResponse])
async def get_quizzes_by_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΟΛΩΝ ΤΩΝ QUIZ ΜΙΑΣ ΕΝΟΤΗΤΑΣ
    """
    result = await db.execute(
        select(Quiz).where(Quiz.lesson_id == lesson_id)
    )
    quizzes = result.scalars().all()
    return quizzes

# ========================================
# 3. GET QUIZ BY ID (WITH QUESTIONS)
# ========================================
@router.get("/quizzes/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΕΝΟΣ QUIZ ΜΕ ΤΙΣ ΕΡΩΤΗΣΕΙΣ ΤΟΥ
    """
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    return quiz

# ========================================
# 4. UPDATE QUIZ (INSTRUCTOR)
# ========================================
@router.put("/quizzes/{quiz_id}", response_model=QuizResponse)
async def update_quiz(
    quiz_id: int,
    quiz_data: QuizUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΕΝΗΜΕΡΩΣΗ QUIZ
    """
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Έλεγχος δικαιωμάτων
    result = await db.execute(select(Lesson).where(Lesson.id == quiz.lesson_id))
    lesson = result.scalar_one_or_none()
    result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = result.scalar_one_or_none()
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update quizzes in your own courses"
        )
    
    update_data = quiz_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(quiz, field, value)
    
    await db.commit()
    await db.refresh(quiz)
    
    return quiz

# ========================================
# 5. DELETE QUIZ (INSTRUCTOR)
# ========================================
@router.delete("/quizzes/{quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_quiz(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΔΙΑΓΡΑΦΗ QUIZ
    """
    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Έλεγχος δικαιωμάτων
    result = await db.execute(select(Lesson).where(Lesson.id == quiz.lesson_id))
    lesson = result.scalar_one_or_none()
    result = await db.execute(select(Course).where(Course.id == lesson.course_id))
    course = result.scalar_one_or_none()
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete quizzes in your own courses"
        )
    
    await db.delete(quiz)
    await db.commit()
    
    return None

# ========================================
# 6. SUBMIT QUIZ (STUDENT)
# ========================================
@router.post("/quizzes/{quiz_id}/submit", response_model=QuizAttemptResponse)
async def submit_quiz(
    quiz_id: int,
    submission: QuizSubmit,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΥΠΟΒΟΛΗ ΑΠΑΝΤΗΣΕΩΝ ΣΕ QUIZ
    """

    result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    if not quiz.is_published:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Quiz is not published yet"
        )
    
    result = await db.execute(select(Lesson).where(Lesson.id == quiz.lesson_id))
    lesson = result.scalar_one_or_none()
    
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == lesson.course_id,
            Enrollment.status == EnrollmentStatus.ACTIVE
        )
    )
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not enrolled in this course"
        )
    
    result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.quiz_id == quiz_id
        )
    )
    attempts = result.scalars().all()
    
    if len(attempts) >= quiz.max_attempts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have reached the maximum number of attempts"
        )
    

    result = await db.execute(
        select(Question).where(Question.quiz_id == quiz_id)
    )
    questions = result.scalars().all()
    

    score = 0
    max_score = 0
    user_answers = submission.answers
    
    for i, question in enumerate(questions):
        max_score += question.points
        if i < len(user_answers) and user_answers[i] == question.correct_answer:
            score += question.points
    
    percentage = int((score / max_score) * 100) if max_score > 0 else 0
    is_passed = percentage >= quiz.passing_score
    

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        max_score=max_score,
        percentage=percentage,
        is_passed=is_passed,
        answers=user_answers,
        completed_at=datetime.now(timezone.utc)
    )
    
    db.add(attempt)
    await db.commit()
    await db.refresh(attempt)
    

    if is_passed:
        result = await db.execute(
            select(Progress).where(
                Progress.user_id == current_user.id,
                Progress.lesson_id == quiz.lesson_id
            )
        )
        progress = result.scalar_one_or_none()
        if progress:
            progress.is_completed = True
            progress.progress_percentage = 100
            progress.completed_at = datetime.now(timezone.utc)
            await db.commit()
    
    return attempt

# ========================================
# 7. GET MY QUIZ ATTEMPTS
# ========================================
@router.get("/quizzes/{quiz_id}/attempts/me", response_model=List[QuizAttemptResponse])
async def get_my_quiz_attempts(
    quiz_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΟΛΩΝ ΤΩΝ ΠΡΟΣΠΑΘΕΙΩΝ ΜΟΥ ΣΕ ΕΝΑ QUIZ
    """
    result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.quiz_id == quiz_id
        ).order_by(QuizAttempt.started_at.desc())
    )
    attempts = result.scalars().all()
    return attempts