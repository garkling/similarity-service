import hashlib
from typing import Annotated

from fastapi import Depends
from langchain_core.documents import Document
from pydantic import BaseModel

from src.modules.embedding_service import EmbeddingService
from src.modules.knowledge_base.kb_repository import KBRepository
from src.modules.pdf_parser import PdfParser
from src.modules.text_cleaning_service import CleaningService
from src.modules.text_partition_service import TextPartitionService


class KBSearchResult(BaseModel):
    id: str
    sentence: str
    page_number: int
    score: float


class KBService:

    def __init__(
            self,
            pdf_parser: Annotated[PdfParser, Depends()],
            text_cleaner: Annotated[CleaningService, Depends()],
            text_partitioner: Annotated[TextPartitionService, Depends()],
            embedder: Annotated[EmbeddingService, Depends()],
            repository: Annotated[KBRepository, Depends()],
    ):
        self.pdf_parser = pdf_parser
        self.text_cleaner = text_cleaner
        self.text_splitter = text_partitioner
        self.embedder = embedder
        self.repository = repository

    async def create(self, filepath, start_page):
        id_prefix = hashlib.md5(filepath.encode('utf-8')).hexdigest()[:8]

        documents = await self._create_documents(filepath, start_page)
        vectors = await self._create_vectors(documents, id_prefix)

        self.repository.upsert(vectors)

    async def _create_documents(self, filepath, start_page):
        documents = []
        for page in await self.pdf_parser.process(filepath, start_page):
            content = self.text_cleaner.clean(page.content)
            for order, sentence in enumerate(self.text_splitter.split_semantically(content), 1):
                sentence = self.text_cleaner.clean(sentence)
                doc = Document(page_content=sentence, metadata=dict(page_number=page.number, order_number=order, original=sentence))
                documents.append(doc)

        return documents

    async def _create_vectors(self, documents: list, id_prefix: str):
        vectors = []
        embeddings = await self.embedder.embed_documents([doc.page_content for doc in documents])
        for i, doc in enumerate(documents):
            id_ = f"{id_prefix}-{doc.metadata['page_number']}-{doc.metadata['order_number']}"
            vec = dict(
                id=id_,
                values=embeddings[i],
                metadata=doc.metadata
            )
            vectors.append(vec)

        return vectors

    async def search(self, query: str, top_n: int = 3, filter_: dict = None):
        query = self.text_cleaner.clean(query)
        vector = await self.embedder.embed_query(query)

        matches = self.repository.query(vector, top_n, filter_)['matches']
        results = []
        for match in matches:
            meta = match['metadata']
            results.append(
                KBSearchResult(
                id=match['id'],
                sentence=meta['original'],
                page_number=meta['page_number'],
                score=match['score'],
            ))

        return results

    def truncate(self) -> bool:
        self.repository.delete(all_=True)
        return True
