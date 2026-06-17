from langchain.messages import SystemMessage, HumanMessage
import json

from app.utils import prompts
from app.agent.models import small_model


def evaluate_info(state: dict):
    """Node to evaluate info quality"""

    gaps = small_model.invoke(
        [SystemMessage(content=prompts.EVALUATE_INFO_SYSTEM_PROMPT)]
        + [
            HumanMessage(
                content=f"""
Original question: {state["question"]}

Queries already searched: 
{"\n".join([f"-{q}" for q in state["queries"]])}

Information already gathered:
{"\n".join([f"- {r.get('title', 'No Title')}: {r.get('content', '')[:50]}" for r in state["search_results"]])}

Based on the above, identify any gaps as a JSON array. If sufficient, return [].
"""
            )
        ]
    ).content

    try:
        gaps = json.loads(gaps)

    except Exception as e:
        print("The following exception encountered while finding gaps:", e)

    return {"gaps": gaps, "queries": gaps}
