from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from app.db.base import Base

# Column → defines DB column
# Integer, String, Text → data types
# ForeignKey → connects tables
# DateTime → timestamp
# func.now() → current time
# Base → ORM base class

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    # 👉 Unique ID for each comment

# primary_key=True → no duplicates
# index=True → fast searching

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # 👉 Who commented

# ForeignKey → links to users table
# nullable=False → required

    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    # 👉 Which post was commented on

# ForeignKey → links to posts table
# nullable=False → required

    text = Column(Text, nullable=False)
    # 👉 The comment text

# Text → long text
# nullable=False → must have comment

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # 👉 When comment was created

    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    # 👉 When comment was last updated