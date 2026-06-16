from langchain.messages import SystemMessage
from langchain_core.runnables import Runnable

from app.utils import prompts


def synthesize_response(state: dict, synthesis_model: Runnable):
    """Node for synthesizing final response"""

    return {
        "final_response": synthesis_model.invoke(
            [SystemMessage(content=prompts.SYNTHESIZE_RESPONSE_SYSTEM_PROMPT)]
            + state["question"]
            + state["search_results"]
        )
    }
