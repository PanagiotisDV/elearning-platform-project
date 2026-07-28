
"""
SCHEMAS ΓΙΑ  ΧΡΗΣΤΗ
Ορίζουν πώς στέλνουμε και παίρνουμε δεδομένα
"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum
import re


class UserRole(str, Enum):
    
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"
   
class UserCreate(BaseModel):
   
    email: EmailStr = Field(
        ..., 
        description="email του χρήστη"
    )
    password: str = Field(
        ..., 
        min_length=8,
        description="κωδικός (τουλάχιστον 8 χαρακτήρες)"
    )
    full_name: str = Field(
        ...,
        description="πλήρες όνομα"
    )
    
    role: UserRole = Field(
        default=UserRole.STUDENT,
        description="ρόλος του χρήστη"
    )
        
   
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
       
        if not re.search(r'[A-Z]', v):
            
            raise ValueError(' κωδικός εμπεριέχει έχει ένα κεφαλαίο γράμμα')
            
        if not re.search(r'[a-z]', v):
            raise ValueError(' κωδικός εμπεριέχει ένα μικρό γράμμα')
        
        if not re.search(r'\d', v):
            raise ValueError('κωδικός εμπεριέχει έναν αριθμό')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('κωδικός εμπεριέχει έναν ειδικό χαρακτήρα')
        
        return v
        


class UserLogin(BaseModel):
    email: EmailStr
    password: str
   

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    
    class Config:
        from_attributes = True
       


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
   