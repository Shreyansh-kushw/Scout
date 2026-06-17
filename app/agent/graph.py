from typing import Literal
from langgraph.graph import StateGraph, START, END

from app.agent.state import ResearchState
from app.agent.nodes.decompose import decompose_query
from app.agent.nodes.evaluate import evaluate_info
from app.agent.nodes.search import search_query
from app.agent.nodes.synthesise import synthesize_response


def should_continue(
    state: ResearchState,
) -> Literal["search_query", "synthesize_response"]:
    """Fuction that looks at the current state of reasoning to decide whether to continue with a tool call or end the reasoning with an answer"""

    if state.get("iterations", 0) >= 3:
        return "synthesize_response"

    if state["gaps"]:
        return "search_query"
    return "synthesize_response"


agent_builder = StateGraph(ResearchState)

agent_builder.add_node("decompose_query", decompose_query)
agent_builder.add_node("evaluate_info", evaluate_info)
agent_builder.add_node("search_query", search_query)
agent_builder.add_node("synthesize_response", synthesize_response)

agent_builder.add_edge(START, "decompose_query")
agent_builder.add_edge("decompose_query", "search_query")
agent_builder.add_edge("search_query", "evaluate_info")
agent_builder.add_conditional_edges(
    "evaluate_info", should_continue, ["search_query", "synthesize_response"]
)
agent_builder.add_edge("synthesize_response", END)

agent = agent_builder.compile()
