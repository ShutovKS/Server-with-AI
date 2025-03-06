from llama_index.core.tools.function_tool import FunctionTool


def duckduckgo_search(
        query: str,
        region: str = "ru-ru",
        max_results: int = 10,
):
    from duckduckgo_search import DDGS

    with DDGS() as ddg:
        results = list(
            ddg.text(
                keywords=query,
                region=region,
                max_results=max_results,
            )
        )
    return results


def get_tools(**kwargs):
    return [
        FunctionTool.from_defaults(
            fn=duckduckgo_search,
            name="duckduckgo_search",
            description="Ищите любой запрос в поисковой системе DuckDuckgo.",
        ),
    ]
