import logging
import os

from llama_index.core.settings import Settings

logger = logging.getLogger("uvicorn")


def init_settings():
    model_provider = os.getenv("LLM_PROVIDER", "huggingface")
    logger.info(f"Инициализация настроек с поставщиком моделей: {model_provider}")

    match model_provider:
        case "huggingface":
            _init_huggingface()
        case "lm-studio":
            _init_lm_studio()

    logger.info("Поставщик моделей инициализирован")

    _init_embed_model()

    Settings.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
    Settings.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "20"))


def _init_huggingface():
    from llama_index.llms.huggingface import HuggingFaceLLM

    logger.info("Инициализация Huggingface LLM")

    Settings.llm = HuggingFaceLLM(
        model_name=os.getenv("LLM_MODEL"),
        tokenizer_name=os.getenv("LLM_MODEL"),
        max_new_tokens=int(os.getenv("LLM_MAX_NEW_TOKENS", "256")),
    )


def _init_lm_studio():
    from llama_index.llms.lmstudio import LMStudio

    logger.info("Инициализация LM Studio LLM")

    Settings.llm = LMStudio(
        model_name=os.getenv("LLM_MODEL"),
        temperature=0.7,
        request_timeout=180,
        timeout=180,
    )


def _init_embed_model():
    logger.info("Инициализация embed модель")

    from llama_index.embeddings.huggingface import HuggingFaceEmbedding

    Settings.embed_model = HuggingFaceEmbedding(
        model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
        backend=os.getenv("EMBEDDING_BACKEND", "torch"),
    )

    logger.info("Embed модель инициализирована")
