from pydantic import BaseModel
from datetime import datetime
# this is your Pydantic schema for Like system (API layer).
# It defines how data comes in and goes out for likes.


class LikeCreate(BaseModel):
    # Used when user likes a post
    post_id: int
    # User is saying:
    # 👉 "I want to like post with ID = 10"
 
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int
    created_at: datetime
#     {
#   "id": 1,
#   "user_id": 5,
#   "post_id": 10,
#   "created_at": "2026-04-13T10:00:00"
# }
    # Used when API returns a like    
    class Config:
        from_attributes = True
        # This allows:
        # SQLAlchemy object → Pydantic response conversion
 
 
class LikeCount(BaseModel):
    post_id: int
    like_count: int
    # Used to return total likes on a post
    # {
    #   "post_id": 10,
    #   "like_count": 25
    # }



#  Pydantic is a Python library used for:

# ✅ Data validation
# ✅ Data parsing
# ✅ Automatic type checking
# 🔥 What are Pydantic Schemas?

# 👉 Schemas = data structure definitions for your API

# They tell:

# What data should come in (request)
# What data should go out (response)