from sqlalchemy import Column, Integer, ForeignKey, DateTime,UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

# This table stores:
# 👉 Who follows whom

# It creates a relationship between users:

# follower → the one who follows
# following → the one being followed
class Follow(Base):
#     Defines a database table
# Inherits from Base → SQLAlchemy ORM model

    __tablename__ = "follows"

    id = Column(Integer, primary_key=True, index=True)
#     Unique ID for each follow relationship
# Indexed for faster lookup

    follower_id = Column(Integer, ForeignKey("users.id"))
#     Refers to users.id
# Represents:
# 👉 User who is following someone

    following_id = Column(Integer, ForeignKey("users.id"))
#     Refers to users.id
# Represents:
# 👉 User who is being followed

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    from sqlalchemy import UniqueConstraint

__table_args__ = (
    UniqueConstraint('follower_id', 'following_id', name='unique_follow'),
)
  # Ensure one user can't like the same post multiple times