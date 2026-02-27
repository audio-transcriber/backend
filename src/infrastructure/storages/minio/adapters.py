from contextlib import suppress

from boto3 import client as boto3_client

from domain.ports import BytesStorage


class MinIOStorage(BytesStorage):
    def __init__(self, client: boto3_client) -> None:
        self._client = client
        self._bucket_name = 'general'  # TODO в дальнейшем привязать к id пользователя
        with suppress(self._client.exceptions.BucketAlreadyOwnedByYou):
            self._client.create_bucket(Bucket=self._bucket_name)

    async def save(self, content: bytes, filename: str) -> None:
        self._client.put_object(Bucket=self._bucket_name, Key=filename, Body=content)

    async def get(self, filename: str, bucket_name: str) -> bytes:
        response = self._client.get_object(Bucket=bucket_name, Key=filename)
        body = response['Body']
        try:
            return body.read()
        finally:
            body.close()
