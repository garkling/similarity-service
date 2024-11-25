import logging
import logging.config as logging_config
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_logger_config, get_config
from src.modules.embedding_service import EmbeddingService
from src.modules.knowledge_base.kb_controller import kb_router
from src.modules.knowledge_base.kb_repository import KBRepository
from src.modules.knowledge_base.kb_service import KBService
from src.modules.pdf_parser import PdfParser
from src.modules.text_cleaning_service import CleaningService
from src.modules.text_partition_service import TextPartitionService


def get_app() -> FastAPI:
    logging_config.dictConfig(get_logger_config().model_dump())
    logger = logging.getLogger(__name__)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> None:
        kb = KBService(
            pdf_parser=PdfParser(),
            text_cleaner=CleaningService(),
            text_partitioner=TextPartitionService(),
            embedder=EmbeddingService(),
            repository=KBRepository()
        )
        logger.info("Started processing the initial whitepaper")
        await kb.create(get_config().initial_whitepaper_url, start_page=2)
        logger.info("Finished processing the initial whitepaper")
        yield

    app = FastAPI(lifespan=lifespan)
    app.include_router(kb_router)

    return app


app = get_app()


@app.get("/health", status_code=200)
async def health():
    return dict(success=True)
