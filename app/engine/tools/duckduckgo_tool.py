from llama_index.core.tools.function_tool import FunctionTool


def duckduckgo_search(
        query: str,
        region: str = "wt-wt",
        max_results: int = 10,
):
    """
    Use this function to search for any query in DuckDuckGo.
    Args:
        query (str): The query to search in DuckDuckGo.
        region Optional(str): The region to be used for the search in [country-language] convention, ex us-en, uk-en, ru-ru, etc...
        max_results Optional(int): The maximum number of results to be returned. Default is 10.
    """
    
    print(f"DuckDuckGo Searching for: {query}")
    
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        raise ImportError(
            "duckduckgo_search package is required to use this function."
            "Please install it by running: `poetry add duckduckgo_search` or `pip install duckduckgo_search`"
        )

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
            description="Search for any query in DuckDuckGo search engine.",
        ),
    ]
