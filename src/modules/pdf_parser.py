import io

import fitz
import httpx
from openai import BaseModel


class Page(BaseModel):
    content: str
    number: int


class PdfParser:

    async def process(self, filepath, start_page):
        if self.is_url(filepath):
            async with httpx.AsyncClient() as client:
                res = await client.get(filepath)
                buffer = io.BytesIO(res.content)
                return self._parse(buffer, start_page)
        else:
            with open(filepath, "rb") as f:
                buffer = io.BytesIO(f.read())
                return self._parse(buffer, start_page)

    def _parse(self, file, start_page):
        doc = fitz.open(stream=file, filetype="pdf")
        for page in doc.pages(start=start_page):
            text = page.get_text("text")
            yield Page(content=text, number=page.number)

    def is_url(self, filepath):
        return 'http' in filepath
