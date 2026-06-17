from langchain.messages import SystemMessage, HumanMessage
from app.utils import prompts

from app.agent import synthesis_model


def synthesize_response(state: dict):
    """Node for synthesizing final response"""

    return {
        "final_response": synthesis_model.invoke(
            [SystemMessage(content=prompts.SYNTHESIZE_RESPONSE_SYSTEM_PROMPT)]
            + [
                HumanMessage(
                    content=f"""
Original question: {state["question"]}

Information already gathered:
{"\n".join([f"- {r.get('title', 'No Title')}: {r.get('content', '')[:50]}" for r in state["search_results"]])}

"""
                )
            ]
        ).content
    }
