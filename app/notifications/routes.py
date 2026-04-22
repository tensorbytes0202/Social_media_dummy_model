from fastapi import APIRouter, Depends, HTTPException
# APIRouter → create routes
# Depends → dependency injection
# HTTPException → error handling
from sqlalchemy.ext.asyncio import AsyncSession
# Async DB session (non-blocking database operations)

from app.db.deps import get_db
# Database session dependency
from app.likes.schemas import LikeCreate, LikeResponse, LikeCount
# Like schemas (request/response models)
from app.likes.service import like_post, unlike_post, get_post_like_count, get_post_likers
# Like service functions
from app.notifications.service import notify_like
# Notification service function
from app.posts.repository import get_post
# Post repository function

router = APIRouter(prefix="/likes", tags=["likes"])
# Creates router for likes
# prefix → URL starts with /likes/
# tags → groups in Swagger UI

# Like a post
@router.post("/", response_model=LikeResponse)
async def like(data: LikeCreate, db: AsyncSession = Depends(get_db)):
    # POST /likes/
    # Creates a like
    
    # In real app, get current user from JWT token
    user_id = 1
    # Hardcoded user ID (replace with actual user from token)
    
    # Get post to find owner
    post = await get_post(db, data.post_id)
    # Fetches post from DB
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    # Checks if post exists
    
    like = await like_post(db, user_id, data.post_id)
    # Creates like
    
    # Create notification for post owner
    if post.user_id != user_id:
        await notify_like(db, post.user_id, user_id, data.post_id)
    # Creates notification if post owner is different from user
    
    return like


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