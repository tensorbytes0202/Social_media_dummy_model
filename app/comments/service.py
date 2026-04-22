from sqlalchemy.ext.asyncio import AsyncSession
# Async DB session (non-blocking database operation s)
from fastapi import HTTPException
# HTTP exceptions (404, 400, 403, etc.)
from app.comments.repository import (
    create_comment,
    get_comment,
    delete_comment,
    get_comment_count,
    get_post_comments,
    update_comment
)
# Repository functions (database operations)

async def create_post_comment(db: AsyncSession, user_id: int, post_id: int, text: str):
#    Function to create a comment
# Takes:
#     db → database session
#     user_id → who is creating comment
#     post_id → which post
#     text → comment content  
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    # Checks if text is:
    # empty ("")
    # or only spaces (" ")
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Comment text cannot exceed 500 characters")
    # Checks length
    
    comment = await create_comment(db, user_id, post_id, text)
    # Calls repository function
    return comment


async def get_post_all_comments(db: AsyncSession, post_id: int):
    # Function to get all comments for a post
    # Takes:
    #     db → database session
    #     post_id → which post
    return await get_post_comments(db, post_id) 

async def get_post_comment_count(db: AsyncSession, post_id: int):
    # Function to get count of comments for a post
    # Takes:
    #     db → database session
    #     post_id → which post
    return await get_comment_count(db, post_id)

async def update_post_comment(db: AsyncSession, comment_id: int, user_id: int, text: str):
    comment = await get_comment(db, comment_id)
    # Function to update a comment
    # Takes:
    #     db → database session
    #     comment_id → which comment
    #     user_id → who is updating comment
    #     text → updated comment content
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # Checks if comment exists
    
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only edit your own comments")
    # Checks if user is authorized to edit comment
    
    if not text or len(text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Comment text cannot be empty")
    # Checks if text is:
    # empty (""")
    # or only spaces (" ")
    
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Comment text cannot exceed 500 characters")
    # Checks length
    
    updated_comment = await update_comment(db, comment_id, text)
    return updated_comment

async def delete_post_comment(db: AsyncSession, comment_id: int, user_id: int):
    comment = await get_comment(db, comment_id)
    # Function to delete a comment
    # Takes:
    #     db → database session
    #     comment_id → which comment
    #     user_id → who is deleting comment
    
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    # Checks if comment exists
    
    if comment.user_id != user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own comments")
    # Checks if user is authorized to delete comment
    
    await delete_comment(db, comment_id)
    # Calls repository function