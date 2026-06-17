from tavily import TavilyClient

from app.utils.config import settings


tavily_client = TavilyClient(api_key=settings.tavily_api_key)


def search_query(state: dict) -> dict:
    """Query searching node."""

    results = []
    queries_to_search = state.get("gaps") if state.get("gaps") else state["queries"]
    for query in queries_to_search:
        print(query)
        response = tavily_client.search(query=query, max_results=5)

        for r in response["results"]:
            content = r.get("content", "")
            if (
                r.get("score", 0) > 0.3
                and 100 < len(content) < 3000
                and "⊤" not in content
                and "∫" not in content
                and "−D/2" not in content
            ):
                results.append(r)

    return {"search_results": results, "iterations": state.get("iterations", 0) + 1}
