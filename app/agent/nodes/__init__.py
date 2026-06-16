from langchain.messages import SystemMessage, ToolMessage
from langchain_core.runnables import Runnable

from app.agent.tools import tavily
from app.utils import prompts
def decompose_query(state: dict, model_with_tools: Runnable) -> list[str]:
    """Decompose query node"""

    return {
        "queries": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content= prompts.DECOMPOSE_QUERY_SYSTEM_PROMPT
                    )
                ]
                + state["question"]
            )
        ]
    }

def search_query(state: dict) -> dict:
    """Query searching node."""

    results = []

    for query in state['queries']:

        observation = tavily.tavily_tool.invoke(query=query)
        results.append([ToolMessage(content=observation)])

    return {
        "search_results": results
    }

def evaluate_info(state: dict, model_with_tools: Runnable):
    """Node to evaluate info quality"""

    return {
        "gaps": model_with_tools.invoke(
            [
                SystemMessage(
                    content=prompts.EVALUATE_INFO_SYSTEM_PROMPT
                )
            ]
            + state["question"]
            + state["queries"]
            + state["search_results"]
        )
    }

def synthesize_response(state: dict, synthesis_model: Runnable):
    """Node for synthesizing final response"""

    return {
        "final_response": synthesis_model.invoke(
            [
                SystemMessage(
                    content=prompts.SYNTHESIZE_RESPONSE_SYSTEM_PROMPT
                )
            ]
            + state["question"]
            + state["search_results"]
        )
    }
    