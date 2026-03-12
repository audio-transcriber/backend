from pathlib import Path

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile, Form, File
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_202_ACCEPTED

from application.containers import TranscriptionContainer
from application.transcription.usecases import TranscriptionUseCase
from infrastructure.docx import DocxConvertor

route = APIRouter(prefix='/transcription', tags=['Transcription'])


@route.post('/transcribe', status_code=HTTP_202_ACCEPTED)
@inject
async def transcribe(
    sid: str = Form(...),
    file: UploadFile = File(...),
    usecase: TranscriptionUseCase = Depends(Provide[TranscriptionContainer.usecase]),
) -> None:
    await usecase.send_transcribe(sid, await file.read(), file.filename)


@route.get('/get_result', status_code=HTTP_200_OK)
@inject
async def get_result(
    filename: str,
    bucket_name: str,
    usecase: TranscriptionUseCase = Depends(Provide[TranscriptionContainer.usecase]),
) -> None:
    return Response(
        content=await usecase.get_result(filename, bucket_name, DocxConvertor()),
        media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        headers={'Content-Disposition': f'attachment; filename={Path(filename).with_suffix(".docx").name}'},
    )
