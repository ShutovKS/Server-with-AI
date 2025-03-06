import logging
import os

from pydantic import BaseModel, validator

logger = logging.getLogger(__name__)


class FileLoaderConfig(BaseModel):
    path: str

    @validator("path", pre=True, always=True)
    def validate_path(cls, v):
        if v == "/path/to/file":
            data_dir = os.getenv("DATA_DIR", ".data")
            return data_dir
        return v


def get_file_documents(config: FileLoaderConfig):
    from llama_index.core.readers import SimpleDirectoryReader

    try:
        file_extractor = None
        reader = SimpleDirectoryReader(
            config.path,
            recursive=True,
            filename_as_id=True,
            raise_on_error=True,
            file_extractor=file_extractor,
        )
        return reader.load_data()
    except Exception as e:
        import sys
        import traceback
        _, _, exc_traceback = sys.exc_info()
        function_name = traceback.extract_tb(exc_traceback)[-1].name
        if function_name == "_add_files":
            logger.warning(
                f"Не удалось загрузить файловые документы, сообщение об ошибке: {e}. Вернуть в виде пустого списка документов."
            )
            return []
        else:
            raise e
