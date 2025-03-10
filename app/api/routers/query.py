import logging
import os
from datetime import datetime
from typing import List

from fastapi import APIRouter
from llama_index.core import Settings
from llama_index.core.agent import AgentRunner
from llama_index.core.base.response.schema import Response
from llama_index.core.tools import BaseTool

from app.api.routers.models import QueryPayload
from app.engine.index import get_index
from app.engine.tools.query_engine import get_query_engine_tool

query_router = r = APIRouter()
logger = logging.getLogger("uvicorn")


@r.post("/complete")
async def query_complete(payload: QueryPayload) -> str:
    time = datetime.now()

    query = payload.query
    verbose = os.getenv("VERBOSE", "False").lower() == "true"
    system_prompt = os.getenv("SYSTEM_PROMPT"),
    
    response: str = (await Settings.llm.acomplete(
        query,
        verbose=verbose,
        system_prompt=system_prompt,
    )).text

    print(f'Time start: {time}')
    print(f'Time end: {datetime.now()}')
    print(f'Time delta: {datetime.now() - time}')

    return response


@r.post("/request-to-stored-index")
async def query_request_to_stored_index(payload: QueryPayload) -> str:
    time = datetime.now()

    query = payload.query
    verbose = os.getenv("VERBOSE", "False").lower() == "true"
    system_prompt = os.getenv("SYSTEM_PROMPT")

    index = get_index()

    query_engine = index.as_query_engine(
        verbose=verbose,
        system_prompt=system_prompt,
    )

    response: Response = await query_engine.aquery(query)

    print(f'Time start: {time}')
    print(f'Time end: {datetime.now()}')
    print(f'Time delta: {datetime.now() - time}')

    return response.response


@r.post("/request-agent")
async def query_request_agent(payload: QueryPayload) -> str:
    time = datetime.now()

    query = payload.query

    verbose = os.getenv("VERBOSE", "False").lower() == "true"
    system_prompt = os.getenv("SYSTEM_PROMPT")

    tools: List[BaseTool] = []
    index = get_index()
    if index is not None:
        query_engine_tool = get_query_engine_tool(index)
        tools.append(query_engine_tool)

    agent = AgentRunner.from_llm(
        llm=Settings.llm,
        tools=tools,
        system_prompt=system_prompt,
        verbose=verbose,
    )

    response: Response = await agent.aquery(query)

    print(f'Time start: {time}')
    print(f'Time end: {datetime.now()}')
    print(f'Time delta: {datetime.now() - time}')

    return response.response
