from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.tools.query_engine import QueryEngineTool


def create_query_engine(index, **kwargs) -> BaseQueryEngine:
    return index.as_query_engine(**kwargs)


def get_query_engine_tool(
        index,
        **kwargs,
) -> QueryEngineTool:
    name = "query_index"

    description = (
        "Используйте этот инструмент для извлечения текстовой информации о законах и юридических вопросах из индекса."
    )

    query_engine = create_query_engine(index, **kwargs)

    return QueryEngineTool.from_defaults(
        query_engine=query_engine,
        name=name,
        description=description,
    )
