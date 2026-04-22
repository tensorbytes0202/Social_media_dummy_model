from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.likes.schemas import LikeCreate, LikeResponse, LikeCount
from app.likes.service import like_post, unlike_post, get_post_like_count, get_post_likers
from app.notifications.service import notify_like
from app.posts.repository import get_post

router = APIRouter(prefix="/likes", tags=["likes"])
# Base URL ban gaya:


# Like a post
@router.post("/", response_model=LikeResponse)
# API: POST /likes/
async def like(data: LikeCreate, db: AsyncSession = Depends(get_db)):
    # Inputs:

    # data.post_id → kaunsa post like karna hai
    # db → database connection
    
    # In real app, get current user from JWT token
    user_id = 1
    # Abhi hardcoded hai (real app me JWT se aayega)
    
    # Get post to find owner
    post = await get_post(db, data.post_id)
    # Check:
    # "Post exist karta hai ya nahi?"
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Agar post nahi mila → error ❌   
    
    like = await like_post(db, user_id, data.post_id)
    # Service call → DB me like save ✅
    
    # Create notification for post owner
    if post.user_id != user_id:
        await notify_like(db, post.user_id, user_id, data.post_id)
    
    return like
#     👉 Agar:

# tum apni post ko like nahi kar rahe ho

# 👉 Tab:

# post owner ko notification jayega

# 💡 Example:

# "User1 liked your post"


# Unlike a post
@router.delete("/{post_id}")
async def unlike(post_id: int, db: AsyncSession = Depends(get_db)):
    
    # In real app, get current user from JWT token
    user_id = 1
    
    await unlike_post(db, user_id, post_id)
    
    return {"message": "Post unliked successfully"}


# Get like count for a post
@router.get("/count/{post_id}", response_model=LikeCount)
async def get_like_count(post_id: int, db: AsyncSession = Depends(get_db)):
    
    like_count = await get_post_like_count(db, post_id)
    
    return {
        "post_id": post_id,
        "like_count": like_count
    }


# Get all users who liked a post
@router.get("/{post_id}", response_model=list[LikeResponse])
async def get_likers(post_id: int, db: AsyncSession = Depends(get_db)):
    
    likes = await get_post_likers(db, post_id)
    
    return likes