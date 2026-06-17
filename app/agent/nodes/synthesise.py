from langchain.messages import SystemMessage, HumanMessage
from app.utils import prompts

from app.agent.agent import synthesis_model


def synthesize_response(state: dict):
    """Node for synthesizing final response"""

    source_text = "\n\n".join(
        [
            f"[{i + 1}] {result.get('title', 'No title')}\nContent: {result.get('content', '')}\nURL: {result.get('url', 'No URL')}"
            for i, result in enumerate(state["search_results"])
        ]
    )

    return {
        "final_response": synthesis_model.invoke(
            [SystemMessage(content=prompts.SYNTHESIZE_RESPONSE_SYSTEM_PROMPT)]
            + [
                HumanMessage(
                    content=f"""
Original question: {state["question"]}

Information already gathered:
{source_text}

"""
                )
            ]
        ).content
    }
