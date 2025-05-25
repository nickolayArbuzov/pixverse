import aio_pika
import json
from src.settings import rabbitmq_settings


async def publish_event(event_type: str, payload: dict, routing_key: str):
    connection = await aio_pika.connect_robust(rabbitmq_settings.rabbitmq_url)
    channel = await connection.channel()
    message = aio_pika.Message(
        body=json.dumps({"event_type": event_type, "payload": payload}).encode(),
        delivery_mode=2
    )
    await channel.default_exchange.publish(message, routing_key=routing_key)
    await connection.close()
