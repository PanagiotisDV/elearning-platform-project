"""
COURSE ENDPOINTS
CRUD για τα μαθήματα
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, require_role
from app.db.session import get_db
from app.models.course import Course
from app.models.user import User
from app.schemas.course import CourseCreate, CourseListResponse, CourseResponse, CourseUpdate

router = APIRouter()


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_data: CourseCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor")),
):
    """
    ΔΗΜΙΟΥΡΓΙΑ ΝΕΟΥ ΜΑΘΗΜΑΤΟΣ
    Μόνο instructors και admins
    """

    new_course = Course(
        title=course_data.title.strip(),
        description=course_data.description.strip() if course_data.description else None,
        level=course_data.level,
        category=course_data.category.strip() if course_data.category else None,
        is_published=course_data.is_published,
        instructor_id=current_user.id,
    )
    db.add(new_course)
    await db.commit()
    await db.refresh(new_course)

    response = CourseResponse.model_validate(new_course)
    response.instructor_name = f"{current_user.first_name} {current_user.last_name}"
    return response


@router.get("/", response_model=List[CourseListResponse])
async def get_courses(
    skip: int = Query(0, ge=0, description="Πόσα να παραλείψει"),
    limit: int = Query(100, ge=1, le=100, description="Πόσα να πάρει"),
    level: Optional[str] = Query(None, description="Φίλτρο επιπέδου"),
    category: Optional[str] = Query(None, description="Φίλτρο κατηγορίας"),
    search: Optional[str] = Query(None, description="Αναζήτηση στον τίτλο"),
    only_published: bool = Query(True, description="Μόνο δημοσιευμένα"),
    my_courses: bool = Query(False, description="Μόνο τα μαθήματα του instructor"),
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user),
):
    """
    ΛΗΨΗ ΛΙΣΤΑΣ ΜΑΘΗΜΑΤΩΝ
    - Φιλτράρισμα κατά επίπεδο, κατηγορία
    - Αναζήτηση στον τίτλο
    - Pagination (skip/limit)
    - my_courses=true: μόνο τα μαθήματα του instructor
    """

    query = select(Course)

    if my_courses:
        if not current_user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
        if current_user.role.value != "instructor":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only instructors can view their own courses",
            )
        query = query.where(Course.instructor_id == current_user.id)

    if only_published:
        query = query.where(Course.is_published == True)
    elif not current_user or current_user.role.value not in ["instructor", "admin"]:
        query = query.where(Course.is_published == True)

    if level:
        query = query.where(Course.level == level)

    if category:
        query = query.where(Course.category == category)

    if search:
        query = query.where(Course.title.ilike(f"%{search}%"))

    query = query.order_by(Course.created_at.desc()).offset(skip).limit(limit)

    result = await db.execute(query)
    courses = result.scalars().all()

    response_list = []
    for course in courses:
        user_result = await db.execute(select(User).where(User.id == course.instructor_id))
        instructor = user_result.scalar_one_or_none()

        course_response = CourseListResponse.model_validate(course)
        course_response.instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown"
        response_list.append(course_response)

    return response_list


@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_active_user),
):
    """
    ΛΗΨΗ ΕΝΟΣ ΜΑΘΗΜΑΤΟΣ ΜΕ ΤΟ ID ΤΟΥ
    """
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if not course.is_published:
        if not current_user or current_user.id != course.instructor_id:
            if not current_user or current_user.role.value != "admin":
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    user_result = await db.execute(select(User).where(User.id == course.instructor_id))
    instructor = user_result.scalar_one_or_none()

    response = CourseResponse.model_validate(course)
    response.instructor_name = f"{instructor.first_name} {instructor.last_name}" if instructor else "Unknown"
    return response


@router.put("/{course_id}", response_model=CourseResponse)
async def update_course(
    course_id: int,
    course_data: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor")),
):
    """
    ΕΝΗΜΕΡΩΣΗ ΜΑΘΗΜΑΤΟΣ
    Μόνο ο instructor που το δημιούργησε ή admin
    """

    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only update your own courses")

    update_data = course_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(course, field, value)

    await db.commit()
    await db.refresh(course)

    response = CourseResponse.model_validate(course)
    response.instructor_name = f"{current_user.first_name} {current_user.last_name}"
    return response


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role("instructor")),
):
    """
    ΔΙΑΓΡΑΦΗ ΜΑΘΗΜΑΤΟΣ
    Μόνο ο instructor που το δημιούργησε ή admin
    """

    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if not course:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    if course.instructor_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own courses")

    await db.delete(course)
    await db.commit()
    return None