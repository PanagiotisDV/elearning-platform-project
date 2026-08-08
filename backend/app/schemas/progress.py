# backend/app/schemas/progress.py
"""
SCHEMAS ΓΙΑ ΤΗΝ ΠΡΟΟΔΟ
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class ProgressUpdate(BaseModel):
    """
    Τι στέλνει ο μαθητής για να ενημερώσει την πρόοδο
    """
    progress_percentage: Optional[float] = Field(
        None, ge=0, le=100,
        description="Ποσοστό προόδου 0-100"
    )
    last_position: Optional[int] = Field(
        None, ge=0,
        description="Τελευταία θέση σε βίντεο (δευτερόλεπτα)"
    )
    is_completed: Optional[bool] = Field(
        None,
        description="True = ολοκλήρωσε την ενότητα"
    )
    
    @field_validator('progress_percentage')
    @classmethod
    def validate_percentage(cls, v: Optional[float]) -> Optional[float]:
        if v is not None:
            if v < 0 or v > 100:
                raise ValueError('Το ποσοστό πρέπει να είναι μεταξύ 0 και 100')
        return v


class ProgressResponse(BaseModel):
    """
    Τι στέλνουμε πίσω για την πρόοδο
    """
    id: int
    user_id: int
    lesson_id: int
    is_completed: bool
    progress_percentage: float
    last_position: int
    started_at: datetime
    updated_at: Optional[datetime]
    completed_at: Optional[datetime]
    lesson_title: Optional[str] = None
    course_title: Optional[str] = None
    
    class Config:
        from_attributes = True

class OverallProgressResponse(BaseModel):
    """
    Συνολική πρόοδος ενός μαθητή σε ένα μάθημα
    """
    course_id: int
    course_title: str
    total_lessons: int
    completed_lessons: int
    progress_percentage: float 
    
    class Config:
        from_attributes = True