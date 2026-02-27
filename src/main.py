import asyncio
from contextlib import asynccontextmanager

import socketio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import application.containers
import infrastructure.containers
from config import minio_settings, rabbitmq_settings
from presentation.http.transcription.route import route as transcription_route

sio_container = infrastructure.containers.SocketIOContainer()
minio_container = infrastructure.containers.MinIOContainer(
    endpoint_url=minio_settings.endpoint_url,
    secret_key=minio_settings.secret_key,
    access_key=minio_settings.access_key,
)
rabbitmq_container = infrastructure.containers.RabbitMQContainer(
    host=rabbitmq_settings.host,
    port=rabbitmq_settings.port,
)
transcription_container = application.containers.TranscriptionContainer(
    sio_container=sio_container,
    bytes_storage_container=minio_container,
    message_broker_container=rabbitmq_container,
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    await rabbitmq_container.init_resources()
    consumer = await rabbitmq_container.consumer()
    consumer_task = asyncio.create_task(
        consumer.consume(
            'transcription_done',
            await transcription_container.usecase(),
        )
    )
    yield
    consumer_task.cancel()
    await rabbitmq_container.shutdown_resources()


def init_fastapi() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
    )
    app.include_router(transcription_route)
    return app


def init_socketio() -> socketio.AsyncServer:
    sio = sio_container.sio()
    return sio


http_app = init_fastapi()
ws_app = init_socketio()
app = socketio.ASGIApp(ws_app, other_asgi_app=http_app)
