# 👉 Uses connection pooling (single shared connection)
# 👉 Handles startup/shutdown lifecycle
# 👉 Provides channel access
# 👉 Safe for high-load FastAPI apps
# """


import aio_pika
from aio_pika import RobustConnection, RobustChannel
from app.core.config import settings


# ==============================
# 🔌 Global Connection Objects
# ==============================

rabbitmq_connection: RobustConnection | None = None
rabbitmq_channel: RobustChannel | None = None

# ==============================
# 🚀 Connect to RabbitMQ
# ==============================
async def connect_rabbitmq() -> None:
    """
    Establish a robust (auto-reconnecting) connection to RabbitMQ
    """

    global rabbitmq_connection, rabbitmq_channel

    try:
        rabbitmq_connection = await aio_pika.connect_robust(
            settings.RABBITMQ_URL,
            timeout=5
        )

        rabbitmq_channel = await rabbitmq_connection.channel()

        # Optional: limit unacknowledged messages (for consumers)

        await rabbitmq_channel.set_qos(prefetch_count=10)

        print("✅ RabbitMQ connected successfully")
    except Exception as e:
        print(f"❌ RabbitMQ connection failed: {e}")
        raise


# ==============================
# 🔌 Get Channel for Producers/Consumers
# ==============================
async def get_rabbitmq_channel() -> RobustChannel:
    """
    Return the shared RabbitMQ channel
    Raises error if not connected
    """
    if rabbitmq_channel is None or rabbitmq_channel.is_closed:
        raise RuntimeError("❌ RabbitMQ not connected")
    return rabbitmq_channel



# ==============================
# 🔌 Close Connection
# ==============================

async def close_rabbitmq() -> None:
    """
    Gracefully close RabbitMQ connection
    """
    global rabbitmq_connection

    if rabbitmq_connection:
        await rabbitmq_connection.close()
        print("🔌 RabbitMQ connection closed")


# ==============================
# 🔁 Dependency (for FastAPI)
# ==============================

async def get_rabbitmq_channel() -> RobustChannel:
    """
    Dependency to get RabbitMQ channel

    Usage:
    channel = Depends(get_rabbitmq_channel)
    """
    if not rabbitmq_channel:
        raise RuntimeError("RabbitMQ is not initialized")

    return rabbitmq_channel


# ==============================
# 📤 Producer Function
# ==============================

async def publish_message(
    routing_key: str,
    message: str,
) -> None:
    """
    Publish message to RabbitMQ

    Args:
        routing_key: Queue name
        message: Message to send
    """

    if not rabbitmq_channel:
        raise RuntimeError("RabbitMQ not connected")

    await rabbitmq_channel.default_exchange.publish(
        aio_pika.Message(body=message.encode()),
        routing_key=routing_key,
    )

# ==============================
# 📥 Consumer Example
# ==============================
async def consume_messages(queue_name: str):
    """
    Example consumer function
    """
    if not rabbitmq_channel:
        raise RuntimeError("RabbitMQ not connected")

    queue = await rabbitmq_channel.declare_queue(queue_name, durable=True)

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                print(f"📩 Received: {message.body.decode()}")

# ==============================
# ✅ Example usage
# ==============================
# In your FastAPI endpoint:

# @app.post("/publish")
# async def publish_test(message: str):
#     await publish_message("notifications", message)
#     return {"status": "published"}

# In your consumer (background worker):

# async def process_message(message: aio_pika.Message):
#     print("Received:", message.body.decode())

# async def start_consumer():
#     channel = await get_rabbitmq_channel()
#     await channel.default_exchange.consume("notifications", process_message)
