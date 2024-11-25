import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel

from src.modules.knowledge_base.kb_service import KBService, KBSearchResult

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

kb_router = APIRouter(prefix="/kb")


class KBCreateRequest(BaseModel):
    filepath: str
    start_page: int = 2


class KBController:

    def __init__(self, kb_service: Annotated[KBService, Depends()]):
        self._service = kb_service

    async def create(self, request: KBCreateRequest):
        await self._service.create(request.filepath, request.start_page)

    async def search(self, query: str, top_n, filters: dict = None) -> list[KBSearchResult]:
        matches = await self._service.search(query, top_n, filters)
        return matches

    def truncate(self):
        self._service.truncate()


@kb_router.post("", status_code=201)
async def create_knowledge_base(
    body: KBCreateRequest,
    controller: Annotated[KBController, Depends()]
):
    await controller.create(body)
    return dict(message="File processed successfully")


@kb_router.get("", status_code=200)
async def search_knowledge_base(
    controller: Annotated[KBController, Depends()],
    q: str = Query(..., min_length=3, max_length=100),
    top_n: int = Query(3),
    page_number: int | None = Query(None, gt=0),
) -> list[KBSearchResult]:
    filters = dict(page_number=page_number) if page_number else None
    return await controller.search(q, top_n, filters)


@kb_router.delete("", status_code=204)
async def truncate_knowledge_base(
    controller: Annotated[KBController, Depends()],
):
    controller.truncate()
    return dict(message="KB truncated successfully")
