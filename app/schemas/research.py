from pydantic import BaseModel

class research(BaseModel):

    question: str
    queries: list[str]
    search_results: list[dict]
    gaps: list[str]
    iterations: int
    final_response: str