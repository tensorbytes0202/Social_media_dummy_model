from sqlalchemy.ext.asyncio import AsyncSession
# Async DB session (non-blocking queries ke liye)
from sqlalchemy import select, delete
 # SQL queries banane ke liye (SELECT & DELETE)
from app.comments.models import Comment
# Comment ORM model (table representation)
from sqlalchemy import func
 # SQL functions like COUNT use karne ke liye

async def create_comment(db: AsyncSession, user_id: int, post_id: int, text: str):
    # Comment object create kar rahe hain (memory me)
    comment = Comment(user_id=user_id, post_id=post_id, text=text)
    # DB me add kiya
    db.add(comment)
    # Commit → save to DB
    await db.commit()
    # Refresh → get saved object with ID
    await db.refresh(comment)
    return comment

async def get_comment(db: AsyncSession, comment_id: int):
    # SELECT query run kar rahe hain jaha id match kare
    result = await db.execute(
        select(Comment).where(Comment.id == comment_id)
    )
    return result.scalar_one_or_none()
       # Agar mila → object return
    # Nahi mila → None return

async def get_post_comments(db: AsyncSession, post_id: int):
        # SELECT all comments where post_id match kare + latest first
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.desc())
    )
    return result.scalars().all()
       # Multiple rows ko list me convert karta hai


# 🔹 Count total comments on a post
async def get_comment_count(db: AsyncSession, post_id: int):
    result = await db.execute(
        select(func.count(Comment.id)).where(Comment.post_id == post_id)
    )
    return result.scalar() or 0
    # Agar None aaye to 0 return (safe handling)


# 🔹 Update existing comment
async def update_comment(db: AsyncSession, comment_id: int, text: str):
     # Pehle comment fetch karte hain
    comment = await get_comment(db, comment_id)
    if comment:
          # Agar comment exist karta hai
        comment.text = text
         # Text update karte hain
        await db.commit()
        await db.refresh(comment)
    return comment

async def delete_comment(db: AsyncSession, comment_id: int):
       # Direct DELETE query run kar rahe hain
    await db.execute(
        delete(Comment).where(Comment.id == comment_id)
    )
    await db.commit()
    # Changes DB me apply (delete confirm)