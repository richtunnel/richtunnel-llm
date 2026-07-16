from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a given city."""
    # Stub — replace with a real weather API call.
    return f"It's sunny and 75°F in {city}."


@tool
def search_docs(query: str) -> str:
    """Search internal documentation for information relevant to the query."""
    # Stub — replace with a real vector search / retriever call.
    return f"Top result for '{query}': (stub) relevant doc snippet."


tools = [get_weather, search_docs]
