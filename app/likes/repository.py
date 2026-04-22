from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.likes.models import Like
from sqlalchemy import func

# Create a like
async def create_like(db: AsyncSession, user_id: int, post_id: int):
    # 👉 User kisi post ko like karta hai
    
    like = Like(
        user_id=user_id,
        post_id=post_id
    )
    # 👉 Ek new like object bana
    
    db.add(like)
    # Object ko DB queue me add kiya (abhi save nahi hua)
    await db.commit()
    # Transaction commit kiya → DB me save hua
    await db.refresh(like)
    # DB se latest data fetch kiya
    
    return like


# Check if user has already liked the post
async def get_like(db: AsyncSession, user_id: int, post_id: int):
    # 👉 SQL banega:
    result = await db.execute(
        select(Like).where(
            (Like.user_id == user_id) & (Like.post_id == post_id)
        )
    )
    
    return result.scalar_one_or_none()
    

    # 👉 Return:

    # Like object → agar exist karta hai
    # None → agar nahi

    # 💡 Use: duplicate like prevent karne ke liye


# Delete a like (unlike)
async def delete_like(db: AsyncSession, user_id: int, post_id: int):
    
    await db.execute(
        delete(Like).where(
            (Like.user_id == user_id) & (Like.post_id == post_id)
        )
    )
    
    await db.commit()


# Get like count for a post
async def get_like_count(db: AsyncSession, post_id: int):
    
    result = await db.execute(
        select(func.count(Like.id)).where(Like.post_id == post_id)
    )
    
    return result.scalar() or 0


# Get all likes for a post
async def get_post_likes(db: AsyncSession, post_id: int):
    
    result = await db.execute(
        select(Like).where(Like.post_id == post_id).order_by(Like.created_at.desc())
    )
    
    return result.scalars().all()