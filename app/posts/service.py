from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.repository import create_post
from app.likes.repository import get_like_count
from app.comments.repository import get_comment_count


async def create_new_post(db: AsyncSession, user_id: int, image_url: str, caption: str):
    # This function:

    # DB me new post create karta hai
    # Fir usme likes & comments count attach karta hai (default = 0)
    
    post = await create_post(db, user_id, image_url, caption)
    # Calls repository → actual DB insert
    
    # Add counts to response
    post.likes_count = 0
    post.comments_count = 0
    # Temporary attributes add kar raha hai (DB me store nahi ho rahe)
    return post


async def get_post_with_counts(db: AsyncSession, post):
    """Add likes and comments count to post object"""
    # Yeh existing post ko enrich karta hai:
    
    likes_count = await get_like_count(db, post.id)
    comments_count = await get_comment_count(db, post.id)
    # DB se count nikal raha hai
    
    # Add as attributes
    post.likes_count = likes_count
    post.comments_count = comments_count
    # Problem:

    # Yeh SQLAlchemy model me defined nahi hai
    # Yeh sirf runtime pe add ho raha hai
    # Serialization (FastAPI response) me issue aa sakta hai
    return post
