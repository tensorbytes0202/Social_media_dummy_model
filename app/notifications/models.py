from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

#This is a SQLAlchemy ORM model for a Notification table — basically 
# used to store user activity notifications (like Instagram / LinkedIn style alerts).
class Notification(Base):

    #This creates a table model
    #It inherits from Base → so SQLAlchemy knows it's a DB table
    
    __tablename__ = "notifications"
    
    id = Column(Integer, primary_key=True, index=True)
    #Unique ID for each notification
    #primary_key=True → no duplicates
    #index=True → faster search
    
    # User who receives the notification
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # User who triggered the notification
    actor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Type of notification: like, comment, follow
    notification_type = Column(String, nullable=False)  # "like", "comment", "follow"
    
    # Reference to post (for like/comment notifications)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    
    # Reference to comment (for comment notifications)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    # Message/content
    message = Column(String, nullable=True)
    
    # Whether notification is read
    is_read = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())