import os
import re
from typing import List, Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.api.routers.chat import chat_request
from app.api.routers.models import ChatData, Message, MessageRole
from app.api.routers.query import query_request
from app.engine.generate import generate_datasource, storage_dir
from app.settings import init_settings


def response_cleaner(response: str) -> str:
    # Удаляем всё между <think> и </think> (с учётом переносов строк)
    cleaned = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)

    # Убираем лишние пробелы и перевод строки
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()

    # Удаляем все теги
    cleaned = re.sub(r'<[^>]*>', '', cleaned)

    # Удаляем слэши
    cleaned = cleaned.replace('\\', '')

    return cleaned


def think_finder(response: str) -> str:
    # Ищем всё между <think> и </think> (с учётом переносов строк)
    think = re.search(r'<think>(.*?)</think>', response, flags=re.DOTALL)
    if think:
        return think.group(1)
    return ''


app = FastAPI()

# Настройка CORS (если необходимо, можно ограничить список разрешённых доменов)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Хранилище истории чата: ключ - chat_id, значение - список сообщений
chat_histories: Dict[str, List[Message]] = {}


@app.on_event("startup")
async def startup_event():
    """
    Инициализация настроек и создание индекса происходит один раз при старте сервера.
    """
    init_settings()
    if not os.path.exists(storage_dir):
        generate_datasource()


# Модель для одиночного запроса
class QueryRequest(BaseModel):
    content: str


@app.post("/query")
async def run_query_endpoint(query: QueryRequest):
    """
    Эндпоинт для одиночного запроса.
    """
    response = await query_request(query.content)

    think = think_finder(response)

    response = response_cleaner(response)

    return {
        "--response--": response,
        "--think--": think
    }


# Модель запроса для чата
class ChatMessage(BaseModel):
    chat_id: str
    content: str


@app.post("/chat")
async def run_chat_endpoint(chat_message: ChatMessage):
    """
    Эндпоинт для общения в чате.
    Пользователь отправляет свой chat_id и сообщение, после чего система
    добавляет сообщение в историю, вызывает chat_request с полным контекстом,
    сохраняет ответ и возвращает его клиенту.
    """
    chat_id = chat_message.chat_id
    user_text = chat_message.content

    # Если история для данного пользователя отсутствует, создаём её
    if chat_id not in chat_histories:
        chat_histories[chat_id] = []

    # Добавляем сообщение пользователя в историю
    chat_histories[chat_id].append(Message(
        role=MessageRole.USER,
        content=user_text,
        annotations=None
    ))

    # Передаём всю историю в chat_request для сохранения контекста
    chat_data = ChatData(data=None, messages=chat_histories[chat_id])
    result = await chat_request(chat_data)

    assistant_response = result.result.content

    think = think_finder(assistant_response)

    assistant_response = response_cleaner(assistant_response)

    # Добавляем ответ ассистента в историю
    chat_histories[chat_id].append(Message(
        role=MessageRole.ASSISTANT,
        content=assistant_response,
        annotations=None
    ))

    return {
        "--response--": assistant_response,
        "--think--": think
    }


# Модель запроса для чата без истории
class ChatEmptyMessage(BaseModel):
    content: str
    system: str


@app.post("/chat-empty")
async def run_chat_empty_endpoint(chat_message: ChatEmptyMessage):
    user_text = chat_message.content

    system_prompt = chat_message.system

    chat = [
        Message(
            role=MessageRole.SYSTEM,
            content=system_prompt,
            annotations=None
        ),
        Message(
            role=MessageRole.USER,
            content=user_text,
            annotations=None
        )
    ]

    # Передаём всю историю в chat_request для сохранения контекста
    chat_data = ChatData(data=None, messages=chat)
    result = await chat_request(chat_data)

    assistant_response = result.result.content

    think = think_finder(assistant_response)

    assistant_response = response_cleaner(assistant_response)

    return {
        "--response--": assistant_response,
        "--think--": think
    }


@app.get("/chat/{chat_id}")
async def get_chat_history(chat_id: str):
    """
    Эндпоинт для получения истории чата по chat_id.
    """
    if chat_id not in chat_histories:
        raise HTTPException(status_code=404, detail="История чата не найдена")
    return {
        "--history--": chat_histories[chat_id]
    }


class InitChatRequest(BaseModel):
    chat_id: str
    system: str


@app.post("/chat/init")
async def init_chat_endpoint(init_chat: InitChatRequest):
    chat_id = init_chat.chat_id
    system_prompt = init_chat.system

    chat_histories[chat_id] = [Message(
        role=MessageRole.SYSTEM,
        content=system_prompt,
        annotations=None
    )]

    return {"message": "Чат инициализирован", "chat_id": chat_id}


if __name__ == "__main__":
    import uvicorn

    host = os.getenv("APP_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", 8000))

    uvicorn.run("server:app", host=host, port=port, reload=True)

# curl.exe -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"text": "*ТЕКСТ ЗАПРОСА*"}'

# curl.exe -X POST http://localhost:8000/chat-empty -H "Content-Type: application/json" -d '{"content": "*ТЕКСТ СООБЩЕНИЯ*", "system": "*ТЕКСТ ПРИВЕТСТВИЯ*"}'

# curl.exe -X POST http://localhost:8000/chat/init -H "Content-Type: application/json" -d '{"chat_id": "*Ид чата*", "system": "*ТЕКСТ ПРИВЕТСТВИЯ*"}'
# curl.exe -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"chat_id": "*Ид чата*", "content": "*ТЕКСТ СООБЩЕНИЯ*"}'
# curl.exe -X GET http://localhost:8000/chat/*Ид чата*
