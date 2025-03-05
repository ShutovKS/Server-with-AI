import logging

from fastapi import APIRouter
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.base.response.schema import Response

from app.engine.index import IndexConfig, get_index

query_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


def get_query_engine() -> BaseQueryEngine:
    index_config = IndexConfig(**{})
    index = get_index(index_config)
    return index.as_query_engine()

async def query_request(
        query: str,
) -> str:
    query_engine = get_query_engine()
    response: Response = await query_engine.aquery(query)
    return response.response


async def query_agent(query: str) -> str:
    from llama_index.core.agent import AgentRunner
    from llama_index.core import Settings
    import os

    agent = AgentRunner.from_llm(
        llm=Settings.llm,
        system_prompt=os.getenv("SYSTEM_PROMPT"),
        verbose=True,
        max_tokens=os.getenv("LLM_MAX_NEW_TOKENS", 100),
    )
    response = agent.query(query)
    return response.response
