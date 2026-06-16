from langchain.messages import SystemMessage, ToolMessage
from langchain_core.runnables import Runnable

from app.agent.tools import tavily

def decompose_query(state: dict, model_with_tools: Runnable) -> list[str]:
    """Decompose query node"""

    return {
        "queries": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="""
You are a Research Query Decomposition Agent.

Your task is to convert a user's question into a list of focused search queries that, when researched together, would provide all information needed to answer the question.

Rules:
- Do NOT answer the question.
- Do NOT explain your reasoning.
- Do NOT provide summaries, analysis, or conclusions.
- Break complex questions into smaller researchable topics.
- Create queries that are specific, factual, and searchable.
- Avoid redundant or overlapping queries.
- If the question involves comparisons, generate queries for each item and for direct comparisons.
- If the question requires current information, include terms indicating recency.
- Generate enough queries to fully research the topic, but no more than necessary.

Output:
Return ONLY a JSON array of strings.

Example:

User:
"Should a startup use LangGraph or CrewAI for building a customer support agent?"

Output:
[
  "What are the core architecture and design principles of LangGraph?",
  "What are the core architecture and design principles of CrewAI?",
  "How does LangGraph support multi-agent workflows?",
  "How does CrewAI support multi-agent workflows?",
  "How do LangGraph and CrewAI compare in production readiness?",
  "What are the strengths and weaknesses of LangGraph for customer support agents?",
  "What are the strengths and weaknesses of CrewAI for customer support agents?",
  "What do recent community reviews say about LangGraph versus CrewAI?"
]
"""
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
                    content="""
You are a Research Gap Analysis Agent.

Your task is to determine whether the collected research is sufficient to answer the original user question.

You will be given:
1. The original user question.
2. The research queries that were executed.
3. The search results gathered from those queries.

Your job is to identify missing information that would prevent a complete, accurate, and well-supported answer to the original question.

Guidelines:
- Evaluate the research against the original question, not against the executed queries.
- Identify important unanswered questions, missing evidence, missing perspectives, missing comparisons, missing recent information, or missing supporting details.
- Only identify gaps that are necessary to answer the original question well.
- Do not suggest additional queries for information that is already sufficiently covered.
- Avoid redundant or highly overlapping gap queries.
- Prefer specific, targeted follow-up queries over broad research topics.
- If the available information is sufficient to answer the original question with high confidence, return an empty list.
- Do not answer the original question.
- Do not summarize the research.
- Do not explain your reasoning.
- Do not include any text other than the required output.
- A gap should only be returned if obtaining the information would materially improve the completeness, accuracy, or confidence of the final answer.

Output:
Return ONLY a JSON array of strings.

Examples:

If information is missing:

[
  "What are the current pricing differences between LangGraph and CrewAI?",
  "What are the production deployment limitations of CrewAI?",
  "What do recent developer reviews say about LangGraph versus CrewAI in production environments?"
]

If the research is sufficient:

[]
"""
                )
            ]
            + state["question"]
            + state["queries"]
            + state["search_results"]
        )
    }

def synthesize_response(state: dict, synthesis_model: Runnable):
    """Node for synthesizing final response"""

    
    