import re

from langchain_experimental.text_splitter import SemanticChunker
from llama_index.core.text_splitter import SentenceSplitter

from src.utils.llm import LLM


class TextPartitionService:

    SENTENCE_SPLIT = re.compile(r"\.\s+")

    def __init__(self, ch_size = 30, overlap_size = 10):
        self._ch_size = ch_size
        self._sentence_splitter = SentenceSplitter(chunk_size=ch_size, chunk_overlap=overlap_size)

    def split_by_sentences(self, text: str):
        split = self._sentence_splitter.split_text(text)
        return filter(lambda s: len(s.split()) > 3, split)

    def split_semantically(self, text: str):
        approximated_number = self.SENTENCE_SPLIT.split(text)
        chunk_number = len(approximated_number) - 2
        split = SemanticChunker(
            LLM.get_embedding_model(),
            number_of_chunks=chunk_number,
            min_chunk_size=self._ch_size

        ).split_text(text)

        return filter(lambda s: len(s.split()) > 3, split)
