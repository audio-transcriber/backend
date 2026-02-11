from aio_pika import connect_robust
from boto3 import client as boto3_client
from botocore.client import Config as BotoConfig
from dependency_injector import containers, providers

from application.transcription.use_cases import TranscriptionUseCase
from infrastructure.messages.rabbitmq.adapters import RabbitMQProducer
from infrastructure.storages.minio.adapters import MinIOStorage


class TranscriptionContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['presentation.transcription.route'])

    bytes_storage_container = providers.DependenciesContainer()
    message_broker_container = providers.DependenciesContainer()

    use_case = providers.Factory(
        TranscriptionUseCase,
        providers.Factory(bytes_storage_container.adapter),
        providers.Factory(
            message_broker_container.producer_adapter,
        ),
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
    producer_adapter = providers.Factory(RabbitMQProducer, producer_client)
