from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.follow.models import Follow
from sqlalchemy import func


async def create_follow(db: AsyncSession, follower_id: int, following_id: int):
    # 👉 Ye function follow relation create karta hai
    """Create follow relationship"""
    follow = Follow(
        follower_id=follower_id,
        following_id=following_id
    )
    # Ek new object bana:

    # "User A follows User B"
    db.add(follow)
    # Object ko DB queue me add kiya (abhi save nahi hua)
    await db.commit()
    # Transaction commit kiya → DB me save hua
    await db.refresh(follow)
    # DB se latest data fetch kiya
    return follow


async def get_follow(db: AsyncSession, follower_id: int, following_id: int):
    # 👉 Check karta hai:

    # "Kya A already B ko follow karta hai?"
    """Check if user already follows another user"""
    result = await db.execute(
        select(Follow).where(
            (Follow.follower_id == follower_id) & 
            (Follow.following_id == following_id)
        )
        # 👉 Check karta hai:

        # "Kya A already B ko follow karta hai?"
    )
    return result.scalar_one_or_none()
    # Return:

    # object → agar follow exist karta hai
    # None → agar nahi karta


async def get_follower_count(db: AsyncSession, user_id: int):
    """Get number of followers for a user"""
    result = await db.execute(
        select(func.count(Follow.id)).where(Follow.following_id == user_id)
    )
    return result.scalar() or 0


async def get_following_count(db: AsyncSession, user_id: int):
    """Get number of users this user is following"""
    result = await db.execute(
        select(func.count(Follow.id)).where(Follow.follower_id == user_id)
    )
    # Count karta hai:

    # "Kitne log is user ko follow karte hain"
    return result.scalar() or 0
    # 👉 Agar result null ho to 0 return karega

async def get_followers(db: AsyncSession, user_id: int):
    """Get list of followers for a user"""
    result = await db.execute(
        select(Follow).where(Follow.following_id == user_id)
    )
    return result.scalars().all()
    # 👉 Return karta hai:

    # "Kaun-kaun is user ko follow karta hai"

async def get_following(db: AsyncSession, user_id: int):
    """Get list of users this user is following"""
    result = await db.execute(
        select(Follow).where(Follow.follower_id == user_id)
    )
    return result.scalars().all()