from abc import ABC, abstractmethod


class BytesStorage(ABC):
    @abstractmethod
    async def save(self, content: bytes, filename: str) -> None:
        pass

    @abstractmethod
    async def get(self, filename: str, bucket_name: str) -> bytes:
        pass


class MessageBrokerProducer(ABC):
    @abstractmethod
    async def send(self, msg: bytes, queue_name: str) -> None:
        pass
