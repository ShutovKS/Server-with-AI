import os

from llama_index.vector_stores.chroma import ChromaVectorStore


def get_vector_store():
    collection_name = os.getenv("CHROMA_COLLECTION", "default")
    chroma_path = os.getenv("CHROMA_PATH")

    if chroma_path:
        store = ChromaVectorStore.from_params(
            persist_dir=chroma_path,
            collection_name=collection_name
        )
    else:
        if not os.getenv("CHROMA_HOST") or not os.getenv("CHROMA_PORT"):
            raise ValueError(
                "Пожалуйста, предоставьте CHROMA_PATH или CHROMA_HOST и CHROMA_PORT"
            )
        store = ChromaVectorStore.from_params(
            host=os.getenv("CHROMA_HOST"),
            port=os.getenv("CHROMA_PORT", "8001"),
            collection_name=collection_name,
        )
    return store
