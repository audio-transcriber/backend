import json

import aio_pika

from domain.ports import MessageBrokerProducer


class RabbitMQProducer(MessageBrokerProducer):
    def __init__(self, client: aio_pika.RobustConnection) -> None:
        self._client = client

    async def send(self, msg: bytes, queue_name: str) -> None:
        channel = await self._client.channel()
        await channel.declare_queue(queue_name, durable=True)

        await channel.default_exchange.publish(
            aio_pika.Message(body=msg, delivery_mode=aio_pika.DeliveryMode.PERSISTENT),
            routing_key=queue_name,
        )


class RabbitMQConsumer:
    def __init__(self, client: aio_pika.RobustConnection) -> None:
        self._client = client

    async def consume(self, queue_name: str, usecase) -> None:  # TODO WTF usecase обязательно должен иметь receive_transcribe???
        channel = await self._client.channel()
        queue = await channel.declare_queue(queue_name, durable=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    body = json.loads(message.body.decode())
                    await usecase.receive_transcribe(body['filename'], body['bucket_name'])
