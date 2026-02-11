from domain.ports import BytesStorage, MessageBrokerProducer


class TranscriptionUseCase:
    def __init__(self, bytes_storage: BytesStorage, message_broker_producer: MessageBrokerProducer) -> None:
        self._bytes_storage = bytes_storage
        self._message_broker_producer = message_broker_producer

    async def transcribe(self, content: bytes, filename: str) -> None:
        await self._bytes_storage.save(content, filename)
        await self._message_broker_producer.send(f'bucket: general: filename: {filename}'.encode(), 'transcription')
