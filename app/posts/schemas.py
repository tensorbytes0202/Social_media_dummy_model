from pydantic import BaseModel
from datetime import datetime
# BaseModel → schema creation
# Field → validation rules
# datetime → timestamp handling
class PostCreate(BaseModel):
    # Used when user creates a post    
    image_url: str
    caption: str
    # Stores image URL
    # Must be at least 5 characters
    # Prevents empty/invalid URLs


class PostResponse(BaseModel):
    # Used when:
    # Showing feed (multiple posts)
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int = 0
    comments_count: int = 0

#     {
#   "id": 1,
#   "user_id": 2,
#   "image_url": "/img.jpg",
#   "caption": "Nice view 🌄",
#   "created_at": "2026-04-14T10:00:00",
#   "likes_count": 50,
#   "comments_count": 10
# }
    
    class Config:
        from_attributes = True


class PostDetailResponse(BaseModel):
    # Used when:
    # Viewing single post in detail
    id: int
    user_id: int
    image_url: str
    caption: str
    created_at: datetime
    likes_count: int
    comments_count: int
    
    class Config:
        from_attributes = True

# User uploads post
#         ↓
# PostCreate (validated)
#         ↓
# Saved in DB
#         ↓
# Feed → PostResponse
#         ↓
# Single post → PostDetailResponse