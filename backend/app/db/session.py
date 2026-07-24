
"""
ΑΣΥΓΧΡΟΝΗ ΣΥΝΔΕΣΗ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
Δημιουργεί τη σύνδεση με PostgreSQL
"""


from sqlalchemy.ext.asyncio import (
    create_async_engine,      
    AsyncSession,              
    async_sessionmaker        
)
from sqlalchemy.orm import declarative_base
from app.core.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
    pool_size=10,
    max_overflow=20,
)    


AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    
)

Base = declarative_base()


async def get_db() -> AsyncSession:
   
    async with AsyncSessionLocal() as session:
               
        try:
            yield session
            await session.commit()
                        
        except Exception:
            await session.rollback()
                       
            raise
            
        finally:
            await session.close()
           