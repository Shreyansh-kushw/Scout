from langchain.messages import SystemMessage, HumanMessage
import json

from app.utils import prompts
from app.agent.agent import small_model


def decompose_query(state: dict) -> list[str]:
    """Decompose query node"""

    return {
        "queries": json.loads(
            small_model.invoke(
                [SystemMessage(content=prompts.DECOMPOSE_QUERY_SYSTEM_PROMPT)]
                + [HumanMessage(content=state["question"])]
            ).content
        )
    }
