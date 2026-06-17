from fastapi import FastAPI, Query, status
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Annotated

from app.agent import agent
from app.schemas.research import ResearchResponse, SourceItem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def home():
    return FileResponse("frontend/index.html")

@app.get("/research", response_model= ResearchResponse)
async def research_query(
    question:  Annotated[str | None, Query(description="Question to be researched.")],
):
    if question:

        response = await agent.ainvoke({"question": question})
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
    
