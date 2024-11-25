from itertools import islice

import pinecone as pc

from src.config import get_config


class KBRepository:

    def __init__(self, dimension=1536):
        self.config = get_config()

        self.index = self.config.pinecone_idx
        self.dimension = dimension
        self.client = pc.Pinecone(api_key=self.config.pinecone_key)

        self.create_index()

    def create_index(self):
        if self.index not in self.client.list_indexes().names():
            self.client.create_index(
                name=self.index,
                dimension=self.dimension,
                metric='cosine',
                spec=pc.ServerlessSpec(cloud='aws', region='us-east-1')
            )

    def upsert(self, vectors: list, batch_size=200):
        index = self.client.Index(self.index)

        iterable = iter(vectors)
        while batch := list(islice(iterable, batch_size)):
            index.upsert(batch)

    def delete(self, ids: list = None, filter_: dict = None, all_=False):
        index = self.client.Index(self.index)

        index.delete(ids=ids, filter=filter_, delete_all=all_)

    def query(self, vector: list[float], top_k: int, filter_: dict = None):
        index = self.client.Index(self.index)

        return index.query(
            vector=vector,
            filter=filter_,
            top_k=top_k,
            include_metadata=True,
        )
