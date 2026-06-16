from langchain.messages import SystemMessage
from langchain_core.runnables import Runnable

from app.utils import prompts


def evaluate_info(state: dict, model_with_tools: Runnable):
    """Node to evaluate info quality"""

    return {
        "gaps": model_with_tools.invoke(
            [SystemMessage(content=prompts.EVALUATE_INFO_SYSTEM_PROMPT)]
            + state["question"]
            + state["queries"]
            + state["search_results"]
        )
    }
