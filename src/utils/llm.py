from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings

from src.config import get_config


class LLM:

    chat_model = 'o1-mini'
    text_model = 'text-embedding-ada-002'

    @staticmethod
    def get_model():
        return ChatOpenAI(
            model=LLM.chat_model,
            temperature=0.1,
            max_tokens=4000,
            max_retries=2,
            openai_api_key=get_config().openapi_key
        )

    @staticmethod
    def get_embedding_model():
        return OpenAIEmbeddings(
            model=LLM.text_model,
            openai_api_key=get_config().openapi_key
        )
