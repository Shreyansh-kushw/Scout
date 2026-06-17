from fastapi import FastAPI, Query, status
from fastapi.exceptions import HTTPException
from typing import Annotated

from app.agent import agent
from app.schemas.research import research

app = FastAPI()

@app.get("/research", response_model= research)
async def research_query(
    question:  Annotated[str | None, Query(description="Question to be researched.")],
):
    if question:

        response = agent.invoke({"question": question})
        result = research(
            question= response["question"],
            queries=response["queries"],
            search_results=response["search_results"],
            gaps = response["gaps"],
            iterations=response["iterations"],
            final_response=response["final_response"],
        )

        return result
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Search query not provided.")
    
