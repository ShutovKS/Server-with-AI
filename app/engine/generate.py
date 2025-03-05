from dotenv import load_dotenv

load_dotenv()

import logging
import os

from llama_index.core.ingestion import DocstoreStrategy, IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.settings import Settings
from llama_index.core.storage import StorageContext
from llama_index.core.storage.docstore import SimpleDocumentStore

from app.engine.loaders import get_documents
from app.engine.vectordb import get_vector_store
from app.settings import init_settings

storage_dir = os.environ.get("STORAGE_DIR", ".storage")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_doc_store():
    if os.path.exists(storage_dir):
        return SimpleDocumentStore.from_persist_dir(storage_dir)
    else:
        return SimpleDocumentStore()


def run_pipeline(docstore, vector_store, documents):
    pipeline = IngestionPipeline(
        transformations=[
            SentenceSplitter(
                chunk_size=Settings.chunk_size,
                chunk_overlap=Settings.chunk_overlap,
            ),
            Settings.embed_model,
        ],
        docstore=docstore,
        docstore_strategy=DocstoreStrategy.UPSERTS_AND_DELETE,  # type: ignore
        vector_store=vector_store,
    )

    nodes = pipeline.run(show_progress=True, documents=documents)

    return nodes


def persist_storage(docstore, vector_store):
    storage_context = StorageContext.from_defaults(
        docstore=docstore,
        vector_store=vector_store,
    )
    storage_context.persist(storage_dir)


def generate_datasource():
    init_settings()
    logger.info("Generate index for the provided data")

    documents = get_documents()

    for doc in documents:
        doc.metadata["private"] = "false"

    doc_store = get_doc_store()
    vector_store = get_vector_store()

    _ = run_pipeline(doc_store, vector_store, documents)

    persist_storage(doc_store, vector_store)

    logger.info("Finished generating the index")


if __name__ == "__main__":
    generate_datasource()
