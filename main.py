from fastapi import FastAPI, Query, status
from fastapi.exceptions import HTTPException
from typing import Annotated

from app.agent import agent
from app.schemas.research import ResearchResponse, SourceItem

app = FastAPI()

@app.get("/research", response_model= ResearchResponse)
async def research_query(
    question:  Annotated[str | None, Query(description="Question to be researched.")],
):
    if question:

        response = agent.invoke({"question": question})
        result = ResearchResponse(
            question= response["question"],
            queries=response["queries"],
            iterations=response["iterations"],
            sources=[SourceItem(
                title=r.get("title", "No title"),
                url= r.get("url", "No URL")
            ) for r in response["search_results"]],
            report=response["final_response"],
        )

        return result
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Search query not provided.")
    
