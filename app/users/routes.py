from fastapi import APIRouter, Depends, HTTPException
# FastAPI ke core tools:
# APIRouter → routes group karne ke liye
# Depends → dependency injection (DB, auth etc.)
# HTTPException → custom error throw karne ke liye

from sqlalchemy.ext.asyncio import AsyncSession
# SQLAlchemy ka async version
# AsyncDB → async database session
# AsyncSession → request-level DB session

from app.db.deps import get_db
# 👉 Dependency function
# Har request ke liye DB session provide karta hai

from app.users.schemas import UserCreate, UserResponse, UserLogin
# Pydantic schemas:
# UserCreate → signup input
# UserLogin → login input
# UserResponse → output format
from app.users.service import register_user, authenticate_user
# Business logic layer
# Route → service call karta hai
# Service → repo + logic handle karta hai
from app.core.security import create_access_token
# JWT token generate karne ke liye
from fastapi import APIRouter
router = APIRouter(prefix="/users", tags=["users"])
# Ye router define karta hai:


@router.post("/signup", response_model=UserResponse)
# response_model:
# Output automatically filter hoga (safe response)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
#     👉 Parameters:

# user → request body (JSON input)
# db → DB session (auto injected)

    new_user = await register_user(
        db,
        user.username,
        user.password
    )
    # Service call:
    # password hash hota hai
    # DB me save hota hai

    return new_user


@router.post("/login")
# POST /users/login
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
# {
#   "username": "aditya",
#   "password": "123456"
# }
    db_user = await authenticate_user(
        db,
        user.username,
        user.password
    )
    
    # Service:
    # DB se user fetch
    # password verify

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        # {
        #   "detail": "Invalid credentials"
        # }

    token = create_access_token({"sub": db_user.username})

    return {"access_token": token}


# Client → /signup
#         ↓
# Route
#         ↓
# Service
#         ↓
# Hash password
#         ↓
# Save in DB
#         ↓
# Return user


# Client → /login
#         ↓
# Route
#         ↓
# Service
#         ↓
# Verify password
#         ↓
# Generate JWT
#         ↓
# Return token

