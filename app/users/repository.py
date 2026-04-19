from sqlalchemy.ext.asyncio import AsyncSession
# Async DB session
# Non-blocking queries (FastAPI async compatible 🚀)

from sqlalchemy import select
from app.users.models import User
# User table model (ORM class)

async def get_user_by_username(db: AsyncSession, username: str):
    # Function:
    # input: username
    # output: user object या None
    """Get user by username"""
    result = await db.execute(
        select(User).where(User.username == username)
    )
    # ये SQL query बनती है:
    # SELECT * FROM users WHERE username = 'aditya';

    return result.scalar_one_or_none()
    # मतलब:
    # अगर 1 user मिला → return user
    # अगर नहीं मिला → return None
    # अगर multiple मिले → error (but unique constraint होने से safe)


async def get_user_by_id(db: AsyncSession, user_id: int):
    """Get user by ID"""
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    # SELECT * FROM users WHERE id = 1;   
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password_hash: str):
    """Create new user"""
    user = User(
        username=username,
        password_hash=password_hash
    )
    # ORM object create (DB row representation)
    db.add(user)
    # Save changes to DB
    await db.commit()
    # Refresh to get generated ID
    # INSERT INTO users (username, password_hash) VALUES (...);
    await db.refresh(user)
    return user
# 🔐 Signup Flow
    # Route → Service → Repo → DB
                      # ↓
                # create_user()
                      # ↓
               # INSERT INTO users
                    #↓
#                 #  return user
# 🔑 Login Flow
# Route → Service → Repo → DB
#                       ↓
#          get_user_by_username()
#                       ↓
#                 SELECT query
#                       ↓
#                 return user


