from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.deps import get_db
from app.posts.schemas import PostCreate, PostResponse
from app.posts.service import create_new_post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    # ➡️ POST endpoint /posts/
    # ➡️ Response will follow PostResponse schema

    user_id = 1
    # ➡️ Input:
    # post → request body (image_url + caption)
    # db → database session (dependency injection)
    new_post = await create_new_post(
        db,
        user_id,
        post.image_url,
        post.caption
    )
    # ➡️ Calls service layer → good architecture ✔️

    return new_post