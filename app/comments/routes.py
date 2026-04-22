from fastapi import APIRouter, Depends
# APIRouter → helps you create modular routes (like a mini app for comments)
# Depends → used for dependency injection (e.g., database connection)
from sqlalchemy.ext.asyncio import AsyncSession
# AsyncSession → async version of SQLAlchemy session (used to interact with DB without blocking)

from app.db.deps import get_db
# Imports a function get_db
# This function provides a database session to your API endpoints
from app.comments.schemas import CommentCreate, CommentResponse, CommentUpdate, CommentCount
# These are Pydantic models (schemas):
# CommentCreate → request body when creating a comment
# CommentResponse → response format
# CommentUpdate → request body for updating
# CommentCount → response format for count
from app.comments.service import (
    create_post_comment,
    get_post_all_comments,
    get_post_comment_count,
    update_post_comment,
    delete_post_comment
)
# Importing business logic functions (service layer)
# Keeps router clean (good practice 👍)

router = APIRouter(prefix="/comments", tags=["comments"])
# Creates a router
# prefix="/comments" → all routes start with /comments
# tags=["comments"] → groups endpoints in Swagger UI

@router.post("/", response_model=CommentResponse)
# Defines a POST endpoint
# URL → /comments/
# response_model → response must match CommentResponse
async def create_comment(data: CommentCreate, db: AsyncSession = Depends(get_db)):
    # data → request body (validated using CommentCreate)
    # db → database session injected automatically using Depends(get_db)
    user_id = 1
    comment = await create_post_comment(db, user_id, data.post_id, data.text)
    # Calls service function to create comment
    # await because function is async
    return comment

@router.get("/{post_id}", response_model=list[CommentResponse])
# Defines a GET endpoint
# URL → /comments/{post_id}
# response_model → returns list of CommentResponse objects
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    # post_id → taken from URL path
    # db → database session
    comments = await get_post_all_comments(db, post_id)
    # Calls service function to get all comments
    return comments

@router.get("/count/{post_id}", response_model=CommentCount)
# Defines a GET endpoint
# URL → /comments/count/{post_id}
# response_model → returns CommentCount object
async def get_comment_count(post_id: int, db: AsyncSession = Depends(get_db)):
    # post_id → taken from URL path
    # db → database session
    comment_count = await get_post_comment_count(db, post_id)
    # Calls service function to get comment count
    return {"post_id": post_id, "comment_count": comment_count}

@router.put("/{comment_id}", response_model=CommentResponse)
# Defines a PUT endpoint
# URL → /comments/{comment_id}
# response_model → response must match CommentResponse
async def update_comment(comment_id: int, data: CommentUpdate, db: AsyncSession = Depends(get_db)):
    # comment_id → taken from URL path
    # data → request body (validated using CommentUpdate)
    # db → database session
    user_id = 1
    comment = await update_post_comment(db, comment_id, user_id, data.text)
    # Calls service function to update comment
    return comment

@router.delete("/{comment_id}")
# Defines a DELETE endpoint
# URL → /comments/{comment_id}
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    # comment_id → taken from URL path
    # db → database session
    user_id = 1
    await delete_post_comment(db, comment_id, user_id)
    # Calls service function to delete comment
    return {"message": "Comment deleted successfully"}