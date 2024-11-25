from src.utils.llm import LLM


class EmbeddingService:

    def __init__(self):
        self.embedder = LLM.get_embedding_model()

    async def embed_documents(self, documents: list[str]):
        return await self.embedder.aembed_documents(documents)

    async def embed_query(self, query: str):
        return await self.embedder.aembed_query(query)
