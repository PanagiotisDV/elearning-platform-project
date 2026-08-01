
"""
PROGRESS ENDPOINTS
Παρακολούθηση προόδου μαθητών
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List
from app.db.session import get_db
from app.models.lesson import Lesson
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.progress import Progress
from app.models.course import Course
from app.models.user import User
from app.schemas.progress import ProgressUpdate, ProgressResponse, OverallProgressResponse
from app.api.deps import get_current_active_user, require_role

router = APIRouter()


@router.put("/lessons/{lesson_id}/progress", response_model=ProgressResponse)
async def update_progress(
    lesson_id: int,
    progress_data: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΕΝΗΜΕΡΩΣΗ ΠΡΟΟΔΟΥ ΣΕ ΜΙΑ ΕΝΟΤΗΤΑ
    """
   
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    

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
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.lesson_id == lesson_id
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        progress = Progress(
            user_id=current_user.id,
            lesson_id=lesson_id
        )
        db.add(progress)
    
    if progress_data.progress_percentage is not None:
        progress.progress_percentage = progress_data.progress_percentage
    
    if progress_data.last_position is not None:
        progress.last_position = progress_data.last_position
    
    if progress_data.is_completed is True:
        progress.is_completed = True
        progress.progress_percentage = 100
        progress.completed_at = func.now()
    
    await db.commit()
    await db.refresh(progress)
    
    return progress


@router.get("/lessons/{lesson_id}/progress", response_model=ProgressResponse)
async def get_my_lesson_progress(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΤΗΣ ΠΡΟΟΔΟΥ ΜΟΥ ΣΕ ΜΙΑ ΕΝΟΤΗΤΑ
    """
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.lesson_id == lesson_id
        )
    )
    progress = result.scalar_one_or_none()
    
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No progress found for this lesson"
        )
    
    return progress


@router.get("/courses/{course_id}/progress", response_model=OverallProgressResponse)
async def get_course_progress(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΣΥΝΟΛΙΚΗΣ ΠΡΟΟΔΟΥ ΜΟΥ ΣΕ ΕΝΑ ΜΑΘΗΜΑ
    """

    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == course_id,
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
        select(Lesson).where(Lesson.course_id == course_id)
    )
    lessons = result.scalars().all()
    total_lessons = len(lessons)
    
    if total_lessons == 0:
        return OverallProgressResponse(
            course_id=course_id,
            course_title=course.title,
            total_lessons=0,
            completed_lessons=0,
            progress_percentage=0
        )
    

    lesson_ids = [lesson.id for lesson in lessons]
    result = await db.execute(
        select(Progress).where(
            Progress.user_id == current_user.id,
            Progress.lesson_id.in_(lesson_ids),
            Progress.is_completed == True
        )
    )
    completed = result.scalars().all()
    completed_lessons = len(completed)

    progress_percentage = (completed_lessons / total_lessons) * 100
    
    return OverallProgressResponse(
        course_id=course_id,
        course_title=course.title,
        total_lessons=total_lessons,
        completed_lessons=completed_lessons,
        progress_percentage=round(progress_percentage, 2)
    )

@router.get("/courses/{course_id}/students/{student_id}/progress")
async def get_student_progress(
    course_id: int,
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΛΗΨΗ ΠΡΟΟΔΟΥ ΕΝΟΣ ΣΥΓΚΕΚΡΙΜΕΝΟΥ ΜΑΘΗΤΗ (για instructor)
    """

    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view progress for your own courses"
        )
    

    result = await db.execute(
        select(Progress).where(
            Progress.user_id == student_id
        )
    )
    progress = result.scalars().all()
    

    result = await db.execute(
        select(Lesson).where(Lesson.course_id == course_id)
    )
    lessons = result.scalars().all()
    total_lessons = len(lessons)
    
    return {
        "student_id": student_id,
        "course_id": course_id,
        "course_title": course.title,
        "total_lessons": total_lessons,
        "completed_lessons": len([p for p in progress if p.is_completed]),
        "progress": progress
    }