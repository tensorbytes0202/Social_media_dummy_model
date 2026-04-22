# User → FastAPI → (check Redis)
#                      ↓
#                Data mila? → yes → return
#                      ↓ no
#                DB / ML model se fetch
#                      ↓
#                Redis me store
#                      ↓
#                User ko response



# 👉 Uses redis.asyncio for non-blocking I/O
# 👉 Handles connection lifecycle (startup/shutdown)
# 👉 Provides reusable dependency
# 👉 Includes basic health check
# """

import redis.asyncio as redis
from app.core.config import settings
from typing import AsyncGenerator

# ==============================
# 🔌 Redis Client Initialization
# ==============================

# 👉 Create Redis client using URL from settings
# Example URL: redis://localhost:6379/0
redis_client: redis.Redis = redis.from_url(
    settings.REDIS_URL,
    encoding="utf-8",        # Auto decode responses to string
    decode_responses=True,   # No need to manually decode bytes
    socket_connect_timeout=5,  # Timeout for connection
    socket_timeout=5,          # Timeout for operations
    retry_on_timeout=True      # Retry if timeout occurs
)
# ==============================
# 🚀 Startup & Shutdown Handlers
# ==============================
async def connect_redis() -> None:
    """
    Establish connection to Redis server
    Called during FastAPI startup
    """
    try:
        # Ping Redis to check connection
        await redis_client.ping()
        print("✅ Redis connected successfully")
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        raise
        
async def close_redis() -> None:
    """
    Gracefully close Redis connection
    Called during FastAPI shutdown
    """
    try:
        await redis_client.close()
        print("🔌 Redis connection closed")
    except Exception as e:
        print(f"⚠️ Error closing Redis: {e}")



# ==============================
# 🔁 Dependency for FastAPI
# ==============================

async def get_redis() -> AsyncGenerator[redis.Redis, None]:
    """
    Dependency to use Redis in routes/services

    Usage:
    redis = Depends(get_redis)
    """
    try:
        yield redis_client
    finally:
        # No need to close here (handled globally)
        pass

# ==============================
# 🧠 Utility Functions (Optional)
# ==============================
async def set_cache(key: str, value: str, expire: int = 60) -> None:
    """
    Store data in Redis with expiration

    Args:
        key: Redis key
        value: Data to store
        expire: Expiry time in seconds (default 60s)
    """
    await redis_client.set(key, value, ex=expire)

async def get_cache(key: str) -> str | None:
    """
    Retrieve data from Redis

    Returns:
        Value if exists, else None
    """
    return await redis_client.get(key)

async def delete_cache(key: str) -> None:
    """
    Delete a key from Redis
    """
    await redis_client.delete(key)  