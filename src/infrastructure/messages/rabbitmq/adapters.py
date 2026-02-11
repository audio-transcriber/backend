import aio_pika

from domain.ports import MessageBrokerProducer


class RabbitMQProducer(MessageBrokerProducer):
    def __init__(self, client: aio_pika.RobustConnection) -> None:
        self._client = client

    async def send(self, msg: bytes, queue_name: str) -> None:
        channel = await self._client.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        await channel.default_exchange.publish(
            aio_pika.Message(body=msg),
            routing_key=queue.name,
        )
