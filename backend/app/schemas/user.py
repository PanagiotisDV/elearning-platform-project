
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
    first_name: str = Field(
        ..., description="Το όνομα"
    )
    last_name: str = Field(
        ..., description="Το επώνυμο"
    )
    
    role: UserRole = Field(
        default=UserRole.STUDENT,
        description="ρόλος του χρήστη"
    )
        
   
    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
       
        if not re.search(r'[A-Z]', v):
            
            raise ValueError(' κωδικός πρέπει να περιέχει έχει ένα κεφαλαίο γράμμα')
            
        if not re.search(r'[a-z]', v):
            raise ValueError(' κωδικός πρέπει να περιέχει ένα μικρό γράμμα')
        
        if not re.search(r'\d', v):
            raise ValueError('κωδικός πρέπει να περιέχει έναν αριθμό')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('κωδικός πρέπει να περιέχει έναν ειδικό χαρακτήρα')
        
        return v


    @field_validator('first_name')
    @classmethod
    def validate_first_name(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('Το όνομα πρέπει να έχει τουλάχιστον 2 χαρακτήρες')
        if not re.match(r'^[a-zA-Z\s.-]+$', v):
            raise ValueError('Το όνομα επιτρέπει μόνο γράμματα, κενά, παύλες και τελείες')
        return v.strip()
    
    @field_validator('last_name')
    @classmethod
    def validate_last_name(cls, v: str) -> str:
        if len(v) < 2:
            raise ValueError('Το επώνυμο πρέπει να έχει τουλάχιστον 2 χαρακτήρες')
        if not re.match(r'^[a-zA-Z\s.-]+$', v):
            raise ValueError('Το επώνυμο επιτρέπει μόνο γράμματα, κενά, παύλες και τελείες')
        return v.strip()    


class UserLogin(BaseModel):
    email: EmailStr
    password: str
   

class UserResponse(BaseModel):
    id: int
    email: str
    first_name: str  
    last_name: str
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
   