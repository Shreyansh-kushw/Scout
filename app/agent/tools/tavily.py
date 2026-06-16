from langchain_tavily import TavilySearch

tavily_tool = TavilySearch(
    max_results=5,
    search_depth="basic",
    topic="general",
)
