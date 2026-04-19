# This is a FastAPI health check endpoint
from fastapi import APIRouter
# 👉 APIRouter is used to:
# Organize routes into modules
# Keep code clean & scalable
router = APIRouter(prefix="/health",tags=["health"])
# What this does:
# prefix="/health"
# → All routes will start with /health
# tags=["health"]
# → Used in Swagger UI (grouping endpoints)

@router.get("/")
# 👉 This means:
# HTTP Method = GET
# Final URL = /health/
async def health():
    # Async function (FastAPI supports async for performance)
    return {"status":"ok"}
    # Returns JSON response: {"status":"ok"}