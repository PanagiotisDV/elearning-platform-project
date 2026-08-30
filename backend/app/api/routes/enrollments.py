
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

# ========================================
# STUDENT: ΕΓΓΡΑΦΗ ΣΕ ΜΑΘΗΜΑ (PENDING)
# ========================================
@router.post("/enroll", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll_in_course(
    enrollment_data: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Ο STUDENT ΣΤΕΛΝΕΙ ΑΙΤΗΜΑ ΕΓΓΡΑΦΗΣ (PENDING)
    """
    # 1. Έλεγχος ότι ο χρήστης είναι student
    if current_user.role.value not in ["student", "admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can enroll in courses"
        )
    
    # 2. Έλεγχος ότι το μάθημα υπάρχει
    result = await db.execute(select(Course).where(Course.id == enrollment_data.course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Course not found"
        )
    
    # 3. Έλεγχος ότι το μάθημα είναι δημοσιευμένο
    if not course.is_published and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not published yet"
        )
    
    # 4. Έλεγχος ότι δεν υπάρχει ήδη εγγραφή
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == enrollment_data.course_id
        )
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        if existing.status == EnrollmentStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You have already sent an enrollment request"
            )
        elif existing.status == EnrollmentStatus.ACTIVE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You are already enrolled in this course"
            )
        elif existing.status == EnrollmentStatus.DROPPED:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Your enrollment was rejected or dropped"
            )
    
    # 5. Δημιουργία εγγραφής (PENDING)
    new_enrollment = Enrollment(
        user_id=current_user.id,
        course_id=enrollment_data.course_id,
        status=EnrollmentStatus.PENDING
    )
    
    db.add(new_enrollment)
    await db.commit()
    await db.refresh(new_enrollment)
    
    return new_enrollment

# ========================================
# STUDENT: ΛΗΨΗ ΕΓΓΡΑΦΩΝ ΜΟΥ
# ========================================
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
        response_list.append(response)
    
    return response_list

# ========================================
# INSTRUCTOR: ΛΗΨΗ PENDING ΑΙΤΗΜΑΤΩΝ
# ========================================
@router.get("/courses/{course_id}/enrollments/pending")
async def get_pending_enrollments(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    Ο INSTRUCTOR ΒΛΕΠΕΙ ΟΛΑ ΤΑ PENDING ΑΙΤΗΜΑΤΑ ΕΓΓΡΑΦΗΣ
    """
    # 1. Βρίσκουμε το μάθημα
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 2. Έλεγχος δικαιωμάτων
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only view pending enrollments for your own courses"
        )
    
    # 3. Λήψη pending εγγραφών με τα στοιχεία των χρηστών
    result = await db.execute(
        select(Enrollment, User)
        .join(User, Enrollment.user_id == User.id)
        .where(Enrollment.course_id == course_id)
        .where(Enrollment.status == EnrollmentStatus.PENDING)
        .order_by(Enrollment.enrolled_at.desc())
    )
    
    # 4. Δημιουργία response με τα στοιχεία του χρήστη
    pending_list = []
    for enrollment, user in result:
        enrollment_data = {
            "id": enrollment.id,
            "user_id": enrollment.user_id,
            "course_id": enrollment.course_id,
            "status": enrollment.status,
            "progress_percentage": enrollment.progress_percentage,
            "enrolled_at": enrollment.enrolled_at,
            "completed_at": enrollment.completed_at,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}",
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }
        pending_list.append(enrollment_data)
    
    return pending_list

# ========================================
# INSTRUCTOR: ΕΓΚΡΙΣΗ ΕΓΓΡΑΦΗΣ
# ========================================
@router.put("/enrollments/{enrollment_id}/approve")
async def approve_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    Ο INSTRUCTOR ΕΓΚΡΙΝΕΙ ΤΗΝ ΕΓΓΡΑΦΗ
    """
    # 1. Βρίσκουμε την εγγραφή
    result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # 2. Βρίσκουμε το μάθημα
    result = await db.execute(select(Course).where(Course.id == enrollment.course_id))
    course = result.scalar_one_or_none()
    
    # 3. Έλεγχος ότι ο instructor έχει το μάθημα
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only approve enrollments for your own courses"
        )
    
    # 4. Έλεγχος ότι είναι σε κατάσταση PENDING
    if enrollment.status != EnrollmentStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Enrollment is not in pending status"
        )
    
    # 5. Έγκριση
    enrollment.status = EnrollmentStatus.ACTIVE
    await db.commit()
    await db.refresh(enrollment)
    
    return {"message": "Enrollment approved successfully"}

# ========================================
# INSTRUCTOR: ΑΠΟΡΡΙΨΗ ΕΓΓΡΑΦΗΣ
# ========================================
@router.put("/enrollments/{enrollment_id}/reject")
async def reject_enrollment(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor"))
):
    """
    Ο INSTRUCTOR ΑΠΟΡΡΙΠΤΕΙ ΤΗΝ ΕΓΓΡΑΦΗ
    """
    # 1. Βρίσκουμε την εγγραφή
    result = await db.execute(select(Enrollment).where(Enrollment.id == enrollment_id))
    enrollment = result.scalar_one_or_none()
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    # 2. Βρίσκουμε το μάθημα
    result = await db.execute(select(Course).where(Course.id == enrollment.course_id))
    course = result.scalar_one_or_none()
    
    # 3. Έλεγχος ότι ο instructor έχει το μάθημα
    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=403,
            detail="You can only reject enrollments for your own courses"
        )
    
    # 4. Έλεγχος ότι είναι σε κατάσταση PENDING
    if enrollment.status != EnrollmentStatus.PENDING:
        raise HTTPException(
            status_code=400,
            detail="Enrollment is not in pending status"
        )
    
    # 5. Απόρριψη
    enrollment.status = EnrollmentStatus.DROPPED
    await db.commit()
    await db.refresh(enrollment)
    
    return {"message": "Enrollment rejected successfully"}

# ========================================
# STUDENT: ΠΑΡΑΙΤΗΣΗ ΑΠΟ ΜΑΘΗΜΑ (μόνο για ACTIVE)
# ========================================
@router.delete("/enrollments/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def drop_course(
    enrollment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    ΠΑΡΑΙΤΗΣΗ ΑΠΟ ΜΑΘΗΜΑ (μόνο αν είναι ACTIVE)
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
    
    if enrollment.status != EnrollmentStatus.ACTIVE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can only drop active enrollments"
        )
    
    enrollment.status = EnrollmentStatus.DROPPED
    await db.commit()
    
    return None