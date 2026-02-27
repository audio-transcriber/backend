import socketio
from aio_pika import connect_robust
from boto3 import client as boto3_client
from botocore.client import Config as BotoConfig
from dependency_injector import containers, providers

from infrastructure.messages.rabbitmq.adapters import RabbitMQProducer, RabbitMQConsumer
from infrastructure.storages.minio.adapters import MinIOStorage


class SocketIOContainer(containers.DeclarativeContainer):
    sio = providers.Singleton(
        socketio.AsyncServer,
        async_mode='asgi',
        transports=['websocket'],
        cors_allowed_origins='*',
    )


class MinIOContainer(containers.DeclarativeContainer):
    endpoint_url = providers.Dependency()
    access_key = providers.Dependency()
    secret_key = providers.Dependency()

    client = providers.Factory(
        boto3_client,
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name='ru-central1',
        config=BotoConfig(signature_version='s3v4'),
    )
    adapter = providers.Factory(MinIOStorage, client)


class RabbitMQContainer(containers.DeclarativeContainer):
    host = providers.Dependency()
    port = providers.Dependency()

    client = providers.Coroutine(
        connect_robust,
        host=host,
        port=port,
    )
    producer_client = providers.Resource(client)
    consumer_client = providers.Resource(client)
    producer = providers.Factory(RabbitMQProducer, producer_client)
    consumer = providers.Factory(RabbitMQConsumer, consumer_client)
