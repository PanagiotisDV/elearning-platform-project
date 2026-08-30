
"""
SCHEMAS ΓΙΑ ΕΓΓΡΑΦΕΣ
"""

from pydantic import BaseModel, Field, ConfigDict  # ← ΠΡΟΣΘΗΚΗ
from typing import Optional
from datetime import datetime
from enum import Enum

class EnrollmentStatus(str, Enum):
    PENDING = "pending"    
    ACTIVE = "active"
    COMPLETED = "completed"
    DROPPED = "dropped"

class EnrollmentCreate(BaseModel):
    """Εγγραφή σε μάθημα"""
    course_id: int = Field(..., gt=0)  

class EnrollmentResponse(BaseModel):
    id: int
    user_id: int
    course_id: int
    status: EnrollmentStatus = Field(default=EnrollmentStatus.PENDING)
    progress_percentage: int
    enrolled_at: datetime
    completed_at: Optional[datetime]
    course_title: Optional[str] = None
    course_instructor: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)  


class EnrollmentUpdate(BaseModel):
    """Ενημέρωση εγγραφής (για instructors)"""
    status: Optional[EnrollmentStatus] = None
    progress_percentage: Optional[int] = Field(None, ge=0, le=100)


class EnrollmentStatistics(BaseModel):
    """Στατιστικά εγγραφών για ένα μάθημα"""
    course_id: int
    course_title: str
    total_enrollments: int
    active_enrollments: int
    completed_enrollments: int
    dropped_enrollments: int
    average_progress: float
    
    @property
    def completion_rate(self) -> float:
        if self.total_enrollments == 0:
            return 0.0
        return round((self.completed_enrollments / self.total_enrollments) * 100, 2)


class EnrollmentFilter(BaseModel):
    """Φίλτρα για αναζήτηση εγγραφών"""
    user_id: Optional[int] = None
    course_id: Optional[int] = None
    status: Optional[EnrollmentStatus] = None
    min_progress: Optional[int] = Field(None, ge=0, le=100)
    max_progress: Optional[int] = Field(None, ge=0, le=100)
    enrolled_after: Optional[datetime] = None
    enrolled_before: Optional[datetime] = None