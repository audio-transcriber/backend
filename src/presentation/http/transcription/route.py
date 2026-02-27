from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile
from starlette.responses import Response
from starlette.status import HTTP_202_ACCEPTED, HTTP_200_OK

from application.transcription.usecases import TranscriptionUseCase
from application.containers import TranscriptionContainer

route = APIRouter(prefix='/transcription', tags=['Transcription'])


@route.post('/transcribe', status_code=HTTP_202_ACCEPTED)
@inject
async def transcribe(
    file: UploadFile,
    usecase: TranscriptionUseCase = Depends(Provide[TranscriptionContainer.usecase]),
) -> None:
    await usecase.send_transcribe(await file.read(), file.filename)


@route.get('/get_result', status_code=HTTP_200_OK)
@inject
async def get_result(
    filename: str,
    bucket_name: str,
    usecase: TranscriptionUseCase = Depends(Provide[TranscriptionContainer.usecase]),
) -> None:
    return Response(
        content=await usecase.get_result(filename, bucket_name),
        media_type="text/plain",
        headers={
            'Content-Disposition': f'attachment; filename={filename}'
        }
    )
