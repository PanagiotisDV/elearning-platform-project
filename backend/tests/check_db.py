# check_db.py
"""
ΕΛΕΓΧΟΣ ΒΑΣΗΣ - ΔΕΣ ΟΛΟΥΣ ΤΟΥΣ ΧΡΗΣΤΕΣ
"""

import asyncio
from sqlalchemy import select, text
from backend.app.db.session import AsyncSessionLocal
from app.models.user import User

async def show_users():
    print("=" * 50)
    print("📊 ΧΡΗΣΤΕΣ ΣΤΗ ΒΑΣΗ")
    print("=" * 50)
    
    async with AsyncSessionLocal() as session:
        # 1. Πόσοι χρήστες υπάρχουν;
        result = await session.execute(select(User))
        users = result.scalars().all()
        print(f"\n✅ Σύνολο χρηστών: {len(users)}")
        
        # 2. Εμφάνισε όλους τους χρήστες
        print("\n📋 ΛΙΣΤΑ ΧΡΗΣΤΩΝ:")
        print("-" * 60)
        for user in users:
            print(f"ID: {user.id}")
            print(f"  Email: {user.email}")
            print(f"  Όνομα: {user.full_name}")
            print(f"  Ρόλος: {user.role.value}")
            print(f"  Ενεργός: {user.is_active}")
            print(f"  Δημιουργία: {user.created_at}")
            print("-" * 60)
        
        # 3. Δες και τους πίνακες της βάσης
        print("\n📁 ΠΙΝΑΚΕΣ ΣΤΗ ΒΑΣΗ:")
        result = await session.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        tables = result.scalars().all()
        for table in tables:
            print(f"  ✅ {table}")

async def main():
    try:
        await show_users()
    except Exception as e:
        print(f"❌ Σφάλμα: {e}")

if __name__ == "__main__":
    asyncio.run(main())