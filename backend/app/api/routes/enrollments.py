
"""
ENROLLMENT ENDPOINTS
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.db.session import get_db
from app.models.course import Course
from app.models.enrollment import Enrollment, EnrollmentStatus
from app.models.user import User
from app.schemas.enrollment import EnrollmentResponse, EnrollmentCreate
from app.api.deps import get_current_active_user, require_role

router = APIRouter()

@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΕΓΓΡΑΦΗ ΣΕ ΜΑΘΗΜΑ
    Μόνο students
    """
   
    if current_user.role.value not in ["student", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses"
        )
    
   
    result = await db.execute(select(Course).where(Course.id == enrollment_data.course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    
    if not course.is_published and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not published yet"
        )
    
    
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == enrollment_data.course_id,
            Enrollment.status != EnrollmentStatus.DROPPED
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already enrolled in this course"
        )
    
    
    new_enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id,
        status=EnrollmentStatus.ACTIVE
    )
    
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    
    return new_enrollment


@router.get("/enrollments/me", response_model=List[EnrollmentResponse])
async def get_my_enrollments(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΛΗΨΗ ΟΛΩΝ ΤΩΝ ΕΓΓΡΑΦΩΝ ΤΟΥ ΧΡΗΣΤΗ
    """
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.user_id == current_user.id)
        .order_by(Enrollment.enrolled_at.desc())
    )
    enrollments = result.scalars().all()
    
    
    response_list = []
    for enrollment in enrollments:
        result = await db.execute(select(Course).where(Course.id == enrollment.course_id))
        course = result.scalar_one_or_none()
        
        response = EnrollmentResponse.model_validate(enrollment)
        response.course_title = course.title if course else "Unknown"
        response.course_instructor = "Unknown"  # Θα το προσθέσουμε αργότερα
        response_list.append(response)
    
    return response_list


@router.get("/courses/{course_id}/enrollments", response_model=List[EnrollmentResponse])
async def get_course_enrollments(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    ΛΗΨΗ ΟΛΩΝ ΤΩΝ ΕΓΓΡΑΦΩΝ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ
    Μόνο ο instructor του μαθήματος ή admin
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
            detail="You can only view enrollments for your own courses"
        )
    
    
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.course_id == course_id)
        .order_by(Enrollment.enrolled_at.desc())
    )
    enrollments = result.scalars().all()
    
    return enrollments


@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_course(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΠΑΡΑΙΤΗΣΗ ΑΠΟ ΜΑΘΗΜΑ
    """
    
    result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enrollment not found"
        )
    
    
    if enrollment.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only drop your own enrollments"
        )
    
    
    enrollment.status = EnrollmentStatus.DROPPED
    await db.commit()
    
    return None