from langchain_tavily import TavilySearch

from app.utils.config import settings

tavily_tool = TavilySearch(
    max_results=5,
    search_depth="basic",
    topic="general",
    tavily_api_key=settings.tavily_api_key,
)
