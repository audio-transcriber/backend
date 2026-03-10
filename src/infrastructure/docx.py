import io

from docx import Document

from domain.ports import BytesConvertor


class DocxConvertor(BytesConvertor):
    async def convert(self, content: bytes) -> bytes:
        text = content.decode()
        doc = Document()
        doc.add_paragraph(text)
        buffer = io.BytesIO()
        doc.save(buffer)
        return buffer.getvalue()

    @property
    def format(self) -> str:
        return 'docx'
