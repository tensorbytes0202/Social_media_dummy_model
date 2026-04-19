from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

    # Column → defines table columns
    # Integer, String, Boolean → data types
    # DateTime → stores time
    # func.now() → auto current timestamp
    # Base → base class for all DB tables 

class User(Base):
# This defines a User table model in SQLAlchemy ORM
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
#     👉 Unique identifier for each user

# primary_key=True → no duplicates
# index=True → faster queries

    username = Column(String, unique=True, index=True, nullable=False)
#     Stores username (like: aditya_123)

# unique=True → no two users can have same username
# index=True → fast search
# nullable=False → required field

    email = Column(String, unique=True, index=True, nullable=False)

#     👉 Stores user email

# Must be unique
# Used for:
# login
# password reset
# Cannot be empty

    password_hash = Column(String, nullable=False)
    # Stores hashed password (NOT plain text)

    full_name = Column(String, nullable=True)

    bio = Column(String, nullable=True)

    profile_picture = Column(String, nullable=True)

    is_active = Column(Boolean, default=True)

    is_verified = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())