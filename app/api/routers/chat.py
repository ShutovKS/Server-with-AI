import logging
from datetime import datetime

from fastapi import APIRouter
from llama_index.core.llms import MessageRole

from app.api.routers.models import (
    ChatData,
    Message,
    Result,
)
from app.engine.engine import get_chat_engine

chat_router = r = APIRouter()

logger = logging.getLogger("uvicorn")


@r.post("/request")
async def chat_request(
        data: ChatData,
) -> Result:
    time = datetime.now()

    last_message_content = data.get_last_message_content()
    messages = data.get_history_messages()

    params = data.data or {}

    chat_engine = get_chat_engine(
        params=params
    )

    response = await chat_engine.achat(last_message_content, messages)

    result = Result(
        result=Message(
            role=MessageRole.ASSISTANT,
            content=response.response
        )
    )

    print(f'Time start: {time}')
    print(f'Time end: {datetime.now()}')
    print(f'Time delta: {datetime.now() - time}')

    return result
