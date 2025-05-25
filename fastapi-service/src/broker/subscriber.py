import aio_pika
from src.broker.handler import on_message
from src.settings import rabbitmq_settings


async def start_consumer():
    connection = await aio_pika.connect_robust(rabbitmq_settings.rabbitmq_url)
    channel = await connection.channel()

    queue = await channel.declare_queue("order.events", durable=True)
    await queue.consume(on_message)
