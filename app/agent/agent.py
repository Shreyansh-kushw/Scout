from langchain.chat_models import init_chat_model

from app.utils.config import settings

small_model = init_chat_model(
    model=settings.evaluation_query_model,
    model_provider="groq",
    temperature=0,
    api_key=settings.groq_api_key,
)

synthesis_model = init_chat_model(
    model=settings.synthesis_model,
    model_provider="google_genai",
    temperature=1,
    api_key=settings.gemini_api_key,
)
