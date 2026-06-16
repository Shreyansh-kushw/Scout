from typing_extensions import Annotated, TypedDict
import operator

class ResearchState(TypedDict):
    question: str
    queries: list[str]
    search_results: Annotated[list[dict], operator.add]
    gaps: list[str]
    iterations: int
    final_response: str
