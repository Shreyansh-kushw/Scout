from typing_extensions import TypedDict


class ResearchState(TypedDict):
    question: str
    queries: list[str]
    search_results: list[dict]
    gaps: list[str]
    iterations: int
    final_response: str
