from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
# APIRouter → routes banane ke liye
# Depends → dependency injection (auto DB dene ke liye)
# AsyncSession → async DB connection

from app.db.deps import get_db
# Ye function DB session provide karega (auto inject hoga)
from app.follow.schemas import FollowCreate, FollowResponse
# FollowCreate → input schema (user kya bhejega)
# FollowResponse → output schema (API kya return karegi)
from app.follow.service import follow_user
# Ye main business logic hai (service layer)

router = APIRouter(prefix="/follow", tags=["follow"])
# Iska matlab:

# Base URL = /follow
# Tag = Swagger docs me grouping

@router.post("/", response_model=FollowResponse)
# 👉 Ye ek POST API hai
# Full URL banega:    
async def follow(data: FollowCreate, db: AsyncSession = Depends(get_db)):
# 👉 Yahan 2 inputs aa rahe hain:

# 📦 data
# Request body se aayega
# Example:
# {
#   "following_id": 5
# }
    follower_id = 1
# 👉 Ye temporary hai:

# Matlab: user 1 sabko follow kar raha hai 😅
# Real app me ye aayega:
# JWT token se
# logged-in user se
    follow = await follow_user(
        db,
        follower_id,
        data.following_id
    )
    # 👉 Ye kya karega:

    # follow_user() ko call karega
    # DB me follow relation create karega     

    return follow