
"""
ΑΣΥΓΧΡΟΝΗ ΣΥΝΔΕΣΗ ΣΤΗ ΒΑΣΗ ΔΕΔΟΜΕΝΩΝ
Δημιουργεί τη σύνδεση με PostgreSQL
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# ===== ΠΑΡΕ ΤΟ URL ΚΑΙ ΚΑΘΑΡΙΣΕ ΤΟ =====
DATABASE_URL = settings.DATABASE_URL

# ΑΦΑΙΡΕΣΕ ΤΟ "DATABASE_URL=" ΑΝ ΥΠΑΡΧΕΙ
if DATABASE_URL.startswith("DATABASE_URL="):
    DATABASE_URL = DATABASE_URL.replace("DATABASE_URL=", "")

# ΑΦΑΙΡΕΣΕ ΤΥΧΟΝ ΚΕΝΑ
DATABASE_URL = DATABASE_URL.strip()

print(f"📌 Clean URL: {DATABASE_URL}")

# ===== ΔΗΜΙΟΥΡΓΙΑ ENGINE =====
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
    pool_size=10,
    max_overflow=20,
)

print("✅ Engine created successfully!")

# ===== SESSION =====
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ===== BASE =====
Base = declarative_base()

# ===== DEPENDENCY =====
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