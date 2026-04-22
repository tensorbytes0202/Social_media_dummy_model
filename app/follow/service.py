from sqlalchemy.ext.asyncio import AsyncSession
# Yahan tum AsyncSession import kar rahe ho

# Ye database se async (non-blocking) tarike se baat karta hai
# Matlab: ek request ke time server block nahi hota → performance better
from app.follow.repository import create_follow
# Yahan tum ek function create_follow import kar rahe ho

# Ye function probably DB me follow relation create karta hai
# Ye repository layer me hai (clean architecture 👍)


async def follow_user(db: AsyncSession, follower_id: int, following_id: int):
    # Ye function tumhara main business logic hai
    # Isme tum follow operation perform karoge
    # Jaise: DB me row insert karna, validation karna, etc.

    return await create_follow(
        db,
        follower_id,
        following_id
    )
# Yahan tum create_follow ko call kar rahe ho
# Aur jo bhi return hoga, use return kar rahe ho
# Simple aur clean 👍