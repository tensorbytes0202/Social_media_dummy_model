from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.base import Base

#This is a SQLAlchemy ORM model for a Like table — basically 
# used to store user activity notifications (like Instagram / LinkedIn style alerts).
#  Instead of storing likes inside the post, we create a separate table → scalable & clean design.    
class Like(Base):
# Defines a table model
# Inherits from Base → tells SQLAlchemy it's a DB table
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
#     Unique ID for each like
# Indexed for fast queries
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     Refers to users table
# Represents:
# 👉 Which user liked the post
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
#     Refers to posts table
# Represents:
# 👉 Which post was liked
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
#     Stores when the like happened
# Auto-filled using func.now()
    
    # Ensure one user can't like the same post multiple times
    __table_args__ = (UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),)
 