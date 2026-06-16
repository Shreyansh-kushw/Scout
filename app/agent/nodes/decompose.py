from langchain.messages import SystemMessage
from langchain_core.runnables import Runnable

from app.utils import prompts


def decompose_query(state: dict, model_with_tools: Runnable) -> list[str]:
    """Decompose query node"""

    return {
        "queries": [
            model_with_tools.invoke(
                [SystemMessage(content=prompts.DECOMPOSE_QUERY_SYSTEM_PROMPT)]
                + state["question"]
            )
        ]
    }
