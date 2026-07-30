"""
SCHEMAS ΓΙΑ ΤΙΣ ΕΝΟΤΗΤΕΣ
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re
class LessonCreate(BaseModel):
    """
    Τι χρειάζεται για να δημιουργήσουμε μια ενότητα
    """
    title: str = Field(..., max_length=200, description="Ο τίτλος της ενότητας")
    description: Optional[str] = Field(None, description="Περιγραφή")
    
    content_type: str = Field(
        default="video",
        description="video, text, quiz, assignment"
    )
    content_url: Optional[str] = Field(None, max_length=500)
    content_text: Optional[str] = None
    
    order: int = Field(default=0, description="Σειρά εμφάνισης")
    duration_minutes: float = Field(default=0, ge=0)
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError('Ο τίτλος πρέπει να έχει τουλάχιστον 3 χαρακτήρες')
        return v
    
    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v: str) -> str:
        allowed = ['video', 'text', 'quiz', 'assignment']
        if v not in allowed:
            raise ValueError(f'Τύπος πρέπει να είναι: {allowed}')
        return v


class LessonUpdate(BaseModel):
    """
    Τι μπορεί να ενημερώσει ένας instructor
    """
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    content_type: Optional[str] = None
    content_url: Optional[str] = Field(None, max_length=500)
    content_text: Optional[str] = None
    order: Optional[int] = Field(None, ge=0)
    duration_minutes: Optional[float] = Field(None, ge=0)


class LessonResponse(BaseModel):
    """
    Τι στέλνουμε πίσω για μια ενότητα
    """
    id: int
    title: str
    description: Optional[str]
    course_id: int
    content_type: str
    content_url: Optional[str]
    content_text: Optional[str]
    order: int
    duration_minutes: float
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True