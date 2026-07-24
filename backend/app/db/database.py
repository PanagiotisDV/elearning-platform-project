"""
ΔΙΑΧΕΙΡΙΣΗ ΒΑΣΗΣ - ΔΗΜΙΟΥΡΓΙΑ ΠΙΝΑΚΩΝ
"""

from app.db.session import engine, Base
import logging

logger = logging.getLogger(__name__)

async def create_tables():
    logger.info("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(" Tables created successfully!")

async def drop_tables():
    logger.warning(" Dropping all tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.warning(" All tables dropped!")