from typing import Any, Dict

from llama_index.core.tools import FunctionTool


def load_data(
        page: str, lang: str = "ru", **load_kwargs: Dict[str, Any]
) -> str:
    """
    Retrieve a Wikipedia page. Useful for learning about a particular concept that isn't private information.

    Args:
        page (str): Title of the page to read.
        lang (str): Language of Wikipedia to read.
    """
    import wikipedia

    wikipedia.set_lang(lang)
    try:
        wikipedia_page = wikipedia.page(page, **load_kwargs, auto_suggest=False)
    except wikipedia.PageError:
        return "Unable to load page. Try searching instead."
    return wikipedia_page.content


def search_data(query: str, lang: str = "ru") -> str:
    """
    Search Wikipedia for a page related to the given query.
    Use this tool when `load_data` returns no results.

    Args:
        query (str): the string to search for
    """
    import wikipedia

    pages = wikipedia.search(query)
    if len(pages) == 0:
        return "No search results."
    return load_data(pages[0], lang)


def get_tools(**kwargs):
    return [
        FunctionTool.from_defaults(
            fn=load_data,
            name="wikipedia_load_data",
            description="Retrieve a Wikipedia page.",
        ),
        FunctionTool.from_defaults(
            fn=search_data,
            name="wikipedia_search_data",
            description="Search Wikipedia for a page related to the given query.",
        ),
    ]
