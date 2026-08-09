"""
AUTHENTICATION ENDPOINTS
Register, Login, Get Current User
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm  
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone, timedelta
from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.refresh_token import RefreshToken
from app.schemas.user import UserCreate, UserLogin, Token, UserResponse
from app.core.security import (
    get_password_hash, 
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.api.deps import get_current_user
from app.core.config import settings

router = APIRouter()


def get_utc_now() -> datetime:
    """Returns current UTC datetime without timezone info (για αποθήκευση σε DB)"""
    return datetime.now(timezone.utc).replace(tzinfo=None)


# ========================================
# REGISTER
# ========================================
@router.post("/register", response_model=UserResponse)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    if len(user_data.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters long"
        )
    
    result = await db.execute(
        select(User).where(User.email == user_data.email.lower())
    )
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed_password = get_password_hash(user_data.password)
    role_value = user_data.role.value if hasattr(user_data.role, "value") else user_data.role
    model_role = UserRole(role_value)
    
    new_user = User(
        email=user_data.email.lower(),
        hashed_password=hashed_password,
        full_name=user_data.full_name,
        role=model_role
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user


# ========================================
# LOGIN (JSON) - Για frontend
# ========================================
@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    LOGIN - Δέχεται JSON (για frontend)
    """
    result = await db.execute(
        select(User).where(User.email == user_data.email.lower())
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    refresh_token_expires = get_utc_now() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    new_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=refresh_token_expires,
        created_at=get_utc_now()
    )
    
    db.add(new_refresh_token)
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ========================================
# LOGIN-FORM - Για Swagger UI
# ========================================
@router.post("/login-form", response_model=Token)
async def login_form(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    LOGIN - Δέχεται form data (για Swagger UI)
    Χρησιμοποιεί username/password από το OAuth2 form
    """
    result = await db.execute(
        select(User).where(User.email == form_data.username.lower())
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    refresh_token_expires = get_utc_now() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    new_refresh_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=refresh_token_expires,
        created_at=get_utc_now()
    )
    
    db.add(new_refresh_token)
    await db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ========================================
# REFRESH TOKEN
# ========================================
@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db)
):
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    current_utc = get_utc_now()
    
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.user_id == int(user_id),
            RefreshToken.is_valid == True,
            RefreshToken.expires_at > current_utc
        )
    )
    stored_token = result.scalar_one_or_none()
    
    if not stored_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    result = await db.execute(
        select(User).where(User.id == int(user_id))
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = create_access_token(
        data={"sub": str(user.id)}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.id)}
    )
    
    stored_token.is_valid = False
    await db.commit()
    
    refresh_token_expires = get_utc_now() + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    
    new_token_record = RefreshToken(
        user_id=user.id,
        token=new_refresh_token,
        expires_at=refresh_token_expires,
        created_at=get_utc_now()
    )
    
    db.add(new_token_record)
    await db.commit()
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# ========================================
# LOGOUT
# ========================================
@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user),
    refresh_token: str = None,
    db: AsyncSession = Depends(get_db)
):
    if refresh_token:
        result = await db.execute(
            select(RefreshToken).where(
                RefreshToken.token == refresh_token,
                RefreshToken.user_id == current_user.id
            )
        )
        stored_token = result.scalar_one_or_none()
        
        if stored_token:
            stored_token.is_valid = False
            await db.commit()
    
    return {"message": "Successfully logged out"}


# ========================================
# GET CURRENT USER
# ========================================
@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    await db.refresh(current_user)
    return current_user