import logging
from typing import Any, List

from llama_index.core.llms import ChatMessage, MessageRole
from pydantic import BaseModel, validator

logger = logging.getLogger("uvicorn")


class QueryPayload(BaseModel):
    query: str


class Message(BaseModel):
    role: MessageRole
    content: str


class ChatData(BaseModel):
    messages: List[Message]
    data: Any = None

    class Config:
        json_schema_extra = {
            "example": {
                "messages": [
                    {
                        "role": "user",
                        "content": "Какие стандарты для букв существуют?",
                    }
                ]
            }
        }

    @validator("messages")
    def messages_must_not_be_empty(cls, v):
        if len(v) == 0:
            raise ValueError("Сообщения не должны быть пустыми")
        return v

    def get_last_message_content(self) -> str:
        if len(self.messages) == 0:
            raise ValueError("В чате нет сообщения")

        last_message = self.messages[-1]
        message_content = last_message.content

        return message_content

    def get_history_messages(
            self,
    ) -> List[ChatMessage]:

        chat_messages = [
            ChatMessage(role=message.role, content=message.content)
            for message in self.messages[:-1]
        ]

        return chat_messages


class Result(BaseModel):
    result: Message
