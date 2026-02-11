from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import minio_settings, rabbitmq_settings
from infrastructure import containers
from presentation.transcription.route import route as transcription_route

minio_container = containers.MinIOContainer(
    endpoint_url=minio_settings.endpoint_url,
    secret_key=minio_settings.secret_key,
    access_key=minio_settings.access_key,
)

rabbitmq_container = containers.RabbitMQContainer(
    host=rabbitmq_settings.host,
    port=rabbitmq_settings.port,
)

transcription_container = containers.TranscriptionContainer(
    bytes_storage_container=minio_container,
    message_broker_container=rabbitmq_container,
)


@asynccontextmanager
async def lifespan(app_: FastAPI) -> None:
    await rabbitmq_container.init_resources()
    yield
    await rabbitmq_container.shutdown_resources()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
)
app.include_router(transcription_route)
