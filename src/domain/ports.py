from abc import ABC, abstractmethod, abstractproperty
from typing import Protocol


class Logger(Protocol):
    @abstractmethod
    def debug(self, msg: str) -> None:
        pass

    @abstractmethod
    def info(self, msg: str) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str) -> None:
        pass

    @abstractmethod
    def exception(self, msg: str) -> None:
        pass

    @abstractmethod
    def error(self, msg: str) -> None:
        pass

    @abstractmethod
    def critical(self, msg: str) -> None:
        pass


class BytesStorage(ABC):
    @abstractmethod
    async def save(self, content: bytes, filename: str) -> None:
        pass

    @abstractmethod
    async def get(self, filename: str, bucket_name: str) -> bytes:
        pass


class BytesConvertor(ABC):
    @abstractmethod
    async def convert(self, content: bytes) -> bytes:
        pass

    @abstractproperty
    def format(self) -> str:
        pass


class MessageBrokerProducer(ABC):
    @abstractmethod
    async def send(self, msg: bytes, queue_name: str) -> None:
        pass
