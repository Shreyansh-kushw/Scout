from langchain.messages import ToolMessage

from app.agent.tools import tavily


def search_query(state: dict) -> dict:
    """Query searching node."""

    results = []

    if not state["gaps"]:
        for query in state["queries"]:
            observation = tavily.tavily_tool.invoke(query=query)
            results.append([ToolMessage(content=observation)])

        return {"search_results": results}

    for gap in state["gaps"]:
        observation = tavily.tavily_tool.invoke(query=gap)
        results.append([ToolMessage(content=observation)])

    return {"search_results": results}
