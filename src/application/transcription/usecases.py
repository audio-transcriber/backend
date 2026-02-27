import json

import socketio

from domain.ports import BytesStorage, MessageBrokerProducer


class TranscriptionUseCase:
    def __init__(
            self,
            sio: socketio.AsyncServer,
            bytes_storage: BytesStorage,
            message_broker_producer: MessageBrokerProducer,
    ) -> None:
        self._sio = sio
        self._bytes_storage = bytes_storage
        self._message_broker_producer = message_broker_producer

    async def send_transcribe(self, content: bytes, filename: str) -> None:
        await self._bytes_storage.save(content, filename)
        msg = {'filename': filename, 'bucket_name': 'general'}
        await self._message_broker_producer.send(json.dumps(msg).encode(), 'transcription_todo')

    async def receive_transcribe(self, filename: str, bucket_name: str) -> None:
        await self._sio.emit('transcribe_done', {'filename': filename, 'bucket_name': bucket_name})

    async def get_result(self, filename: str, bucket_name: str) -> bytes:
        return await self._bytes_storage.get(filename, bucket_name)
