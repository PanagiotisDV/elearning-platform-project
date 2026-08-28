"""
SCHEMAS ΓΙΑ ΤΑ ΜΑΘΗΜΑΤΑ
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class CourseCreate(BaseModel):
    """
    Τι χρειάζεται για να δημιουργήσουμε ένα μάθημα
    """
    title: str = Field(
        ..., 
        max_length=200,
        description="Ο τίτλος του μαθήματος"
    )
    description: Optional[str] = Field(
        None, 
        description="Η περιγραφή του μαθήματος"
    )
    level: str = Field(
        default="beginner",
        description="Επίπεδο: beginner, intermediate, advanced"
    )
    category: Optional[str] = Field(
        None, 
        max_length=100,
        description="Η κατηγορία του μαθήματος"
    )
    
    is_published: bool = Field(
        default=False,
        description="True = δημοσιευμένο, False = draft"
    )
    

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """
        Ελέγχει αν ο τίτλος είναι έγκυρος
        """
        v = v.strip()
        

        if len(v) < 3:
            raise ValueError('Ο τίτλος πρέπει να έχει τουλάχιστον 3 χαρακτήρες')
        
     
        if re.search(r'[<>{}]', v):
            raise ValueError('Ο τίτλος δεν μπορεί να έχει < > { }')
        
        return v
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v: str) -> str:
        allowed_levels = ['beginner', 'intermediate', 'advanced']
        if v.lower() not in allowed_levels:
            raise ValueError(f'Το επίπεδο πρέπει να είναι ένα από: {allowed_levels}')
        return v.lower()


class CourseUpdate(BaseModel):
    """
    ενημερώνεται από instructor
    """
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    level: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    is_published: Optional[bool] = None
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed_levels = ['beginner', 'intermediate', 'advanced']
            if v.lower() not in allowed_levels:
                raise ValueError(f'Το επίπεδο πρέπει να είναι ένα από: {allowed_levels}')
            return v.lower()
        return v


class CourseResponse(BaseModel):
   
    id: int
    title: str
    description: Optional[str]
    instructor_id: int
    instructor_name: Optional[str] = None  
    is_published: bool
    level: str
    category: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True



class CourseListResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    instructor_name: Optional[str] = None
    level: str
    category: Optional[str]
    is_published: bool
    
    class Config:
        from_attributes = True