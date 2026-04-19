from pydantic import BaseModel

# 👉 Meaning:
# BaseModel → used to create schemas
# Field → used for validation
class FollowCreate(BaseModel):
    following_id: int


class FollowResponse(BaseModel):

    id: int
    follower_id: int
    following_id: int
    # {
    # "id": 1,
    # "follower_id": 2,
    # "following_id": 5,
    # "created_at": "2026-04-14T10:00:00"
    # }

    class Config:
        from_attributes = True

        # 👉 This allows:

        # SQLAlchemy model → Pydantic schema conversion