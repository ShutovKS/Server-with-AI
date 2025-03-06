from typing import Any, Dict

from llama_index.core.tools import FunctionTool


def load_data(
        page: str, lang: str = "ru", **load_kwargs: Dict[str, Any]
) -> str:
    import wikipedia
    wikipedia.set_lang(lang)
    try:
        wikipedia_page = wikipedia.page(page, **load_kwargs, auto_suggest=False)
    except wikipedia.PageError:
        return "Невозможно загрузить страницу. Попробуйте искать вместо этого."
    return wikipedia_page.content


def search_data(query: str, lang: str = "ru") -> str:
    import wikipedia
    pages = wikipedia.search(query)
    if len(pages) == 0:
        return "Нет результатов поиска."
    return load_data(pages[0], lang)


def get_tools(**kwargs):
    return [
        FunctionTool.from_defaults(
            fn=load_data,
            name="wikipedia_load_data",
            description="Получить страницу Википедии.",
        ),
        FunctionTool.from_defaults(
            fn=search_data,
            name="wikipedia_search_data",
            description="Поиск страницы Википедии по данным с запроса.",
        ),
    ]
