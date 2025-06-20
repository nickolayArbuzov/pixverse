import aio_pika
from src.broker.handler import on_message
from src.settings import rabbitmq_settings


async def start_consumer():
    connection = await aio_pika.connect_robust(rabbitmq_settings.RABBITMQ_URL)
    channel = await connection.channel()

    await channel.set_qos(prefetch_count=1)

    queue = await channel.declare_queue("playwright.events", durable=True)
    await queue.consume(on_message)
