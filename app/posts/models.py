from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
# This table stores:
# 👉 User posts (images + captions)

# Every time a user uploads something → a row is created here.

class Post(Base):
# Defines a database table using SQLAlchemy ORM
# Inherits from Base

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)

# Unique ID for each post
# Indexed → fast search

    user_id = Column(Integer, ForeignKey("users.id"))
#     Links post to a user
# Represents:
# # 👉 Who created the post

    image_url = Column(String)
    # Stores image location (not actual image)

    caption = Column(String)

#     Text content of post
# Example:
# 👉 "Enjoying sunset 🌇"

    created_at = Column(DateTime(timezone=True), server_default=func.now())
#     Stores when post was created
# Automatically filled