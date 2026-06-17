from pydantic import BaseModel

class ResearchRequest(BaseModel):

    question: str

class SourceItem(BaseModel):
    title: str
    url: str

class ResearchResponse(BaseModel):

    question: str
    queries: list[str]
    iterations: int
    sources: list[SourceItem]
    report: str