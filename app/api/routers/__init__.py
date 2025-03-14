from fastapi import APIRouter

from .chat import chat_router  # noqa: F401
from .query import query_router  # noqa: F401

api_router = APIRouter()
api_router.include_router(chat_router, prefix="/chat")
api_router.include_router(query_router, prefix="/query")
