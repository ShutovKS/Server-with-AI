import logging
from typing import Optional

from llama_index.core import VectorStoreIndex
from llama_index.core.callbacks import CallbackManager
from pydantic import BaseModel, Field

from app.engine.vectordb import get_vector_store

logger = logging.getLogger("uvicorn")


class IndexConfig(BaseModel):
    callback_manager: Optional[CallbackManager] = Field(
        default=None,
    )


def get_index(config: IndexConfig = None):
    if config is None:
        config = IndexConfig()

    logger.info("Connecting vector store...")

    store = get_vector_store()
    index = VectorStoreIndex.from_vector_store(
        store,
        callback_manager=config.callback_manager,
    )

    logger.info("Finished load index from vector store.")

    return index