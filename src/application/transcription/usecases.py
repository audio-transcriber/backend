import json

import socketio

from domain.ports import BytesConvertor, BytesStorage, Logger, MessageBrokerProducer


class TranscriptionUseCase:
    def __init__(
        self,
        sio: socketio.AsyncServer,
        bytes_storage: BytesStorage,
        message_broker_producer: MessageBrokerProducer,
        logger: Logger,
    ) -> None:
        self._sio = sio
        self._bytes_storage = bytes_storage
        self._message_broker_producer = message_broker_producer
        self._logger = logger

    async def send_transcribe(self, content: bytes, filename: str) -> None:
        await self._bytes_storage.save(content, filename)
        self._logger.info(f'Файл {filename} добавлен в хранилище')
        msg = {'filename': filename, 'bucket_name': 'general'}
        await self._message_broker_producer.send(json.dumps(msg).encode(), 'transcription_todo')
        self._logger.info(f'Запрос на обработку {filename} отправлен')

    async def receive_transcribe(self, filename: str, bucket_name: str) -> None:
        await self._sio.emit('transcribe_done', {'filename': filename, 'bucket_name': bucket_name})
        self._logger.info(f'Событие об успешной обработке {filename} отправлено')

    async def get_result(self, filename: str, bucket_name: str, bytes_convertor: BytesConvertor) -> bytes:
        txt_bytes = await self._bytes_storage.get(filename, bucket_name)
        converted_bytes = await bytes_convertor.convert(txt_bytes)
        self._logger.info(f'Файл {filename} успешно преобразован в формат {bytes_convertor.format}')
        return converted_bytes
