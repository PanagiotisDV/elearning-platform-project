
"""
LESSON ENDPOINTS
CRUD για τις ενότητες
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.lesson import LessonCreate, LessonUpdate, LessonResponse
from app.api.deps import get_current_active_user, require_role

router = APIRouter()


@router.post("/courses/{course_id}/lessons", response_model=LessonResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    course_id: int,
    lesson_data: LessonCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΔΗΜΙΟΥΡΓΙΑ ΝΕΑΣ ΕΝΟΤΗΤΑΣ
    Μόνο instructors και admins
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
            detail="You can only add lessons to your own courses"
        )
    
  
    new_lesson = Lesson(
        title=lesson_data.title.strip(),
        description=lesson_data.description.strip() if lesson_data.description else None,
        course_id=course_id,
        content_type=lesson_data.content_type,
        content_url=lesson_data.content_url,
        content_text=lesson_data.content_text,
        order=lesson_data.order,
        duration_minutes=lesson_data.duration_minutes
    )
    
    db.add(new_lesson)
    await db.commit()
    await db.refresh(new_lesson)
    
    return new_lesson


@router.get("/courses/{course_id}/lessons", response_model=List[LessonResponse])
async def get_lessons_by_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΟΛΩΝ ΤΩΝ ΕΝΟΤΗΤΩΝ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ
    """
  
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
  
    if current_user.role.value not in ["admin", "instructor"]:
        pass
    
  
    result = await db.execute(
        select(Lesson)
        .where(Lesson.course_id == course_id)
        .order_by(Lesson.order)
    )
    lessons = result.scalars().all()
    
    return lessons


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
async def get_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΜΙΑΣ ΕΝΟΤΗΤΑΣ ΜΕ ΤΟ ID ΤΗΣ
    """
    result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = result.scalar_one_or_none()
    
    if not lesson:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    return lesson


@router.put("/lessons/{lesson_id}", response_model=LessonResponse)
async def update_lesson(
    lesson_id: int,
    lesson_data: LessonUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΕΝΗΜΕΡΩΣΗ ΕΝΟΤΗΤΑΣ
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
            detail="You can only update lessons in your own courses"
        )
    

    update_data = lesson_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(lesson, field, value)
    
    await db.commit()
    await db.refresh(lesson)
    
    return lesson


@router.delete("/lessons/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lesson(
    lesson_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΔΙΑΓΡΑΦΗ ΕΝΟΤΗΤΑΣ
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
            detail="You can only delete lessons in your own courses"
        )
    
    await db.delete(lesson)
    await db.commit()
    
    return None