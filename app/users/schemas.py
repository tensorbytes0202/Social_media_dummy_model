from pydantic import BaseModel
from datetime import datetime

# BaseModel → schema banane ke liye
# Field → validation
# datetime → timestamp
# List → multiple item

class UserCreate(BaseModel):
    username: str
    password: str
# {
#   "username": "aditya",
#   "password": "123456"
# }

class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class PostInProfile(BaseModel):
    id: int
    image_url: str
    caption: str
    created_at: datetime
    # id → post ID
    # image_url → image
    # caption → text
    # created_at → time
    likes_count: int = 0
    comments_count: int = 0
    # Computed values
    # (not stored directly in DB)
    
    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    id: int
    username: str
    followers_count: int
    following_count: int
    posts_count: int
    posts: list[PostInProfile] = []

    class Config:
        from_attributes = True

#         {
#   "id": 1,
#   "username": "aditya",
#   "followers_count": 120,
#   "following_count": 80,
#   "posts_count": 5,
#   "posts": [
#     {
#       "id": 10,
#       "image_url": "/img.jpg",
#       "caption": "Trip 🚀",
#       "created_at": "2026-04-14T10:00:00",
#       "likes_count": 50,
#       "comments_count": 10
#     }
#   ]
# }

# User registers → UserCreate
#         ↓
# Login → UserLogin
#         ↓
# Fetch profile → UserProfileResponse
#         ↓
# Posts embedded → PostInProfile