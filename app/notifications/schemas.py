from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class NotificationResponse(BaseModel):
    id: int
    recipient_id: int
    # Who receives notification
    actor_id: int
    # Who triggered it
    notification_type: str  # "like", "comment", "follow"
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    # Optional because:

    # Like → only post_id
    # Comment → post_id + comment_id
    # Follow → none
    message: Optional[str] = None
    is_read: bool
    # Seen/unseen status
    created_at: datetime
    
    class Config:
        from_attributes = True
        # Converts SQLAlchemy → JSON automatically


class NotificationWithActor(BaseModel):
    id: int
    recipient_id: int
    actor_id: int
    actor_username: str
    notification_type: str
    post_id: Optional[int] = None
    comment_id: Optional[int] = None
    message: Optional[str] = None
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class NotificationListResponse(BaseModel):
    notifications: list[NotificationWithActor]
    total: int
    unread_count: int
#     {
#   "notifications": [
#     {
#       "id": 1,
#       "actor_username": "rahul",
#       "notification_type": "like",
#       "post_id": 10,
#       "is_read": false
#     }
#   ],
#   "total": 20,
#   "unread_count": 5
# }
    class Config:
        from_attributes = True


class MarkNotificationAsRead(BaseModel):
    is_read: bool



#     Defines all API structures for notifications system

# Covers:

# Single notification
# Notification with user info
# List response (with counts)
# Update (mark as read)

#------------------------------------------------------------------------------------------

# User likes post
#         ↓
# Notification created
#         ↓
# User opens app
#         ↓
# GET /notifications → NotificationListResponse
#         ↓
# User clicks notification
#         ↓
# PATCH → MarkNotificationAsRead