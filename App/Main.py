from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from App.config import settings
from App.Routes import router
from App.storage import ensure_directories

@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_directories()
    yield


app = FastAPI(
    title="ComicCraft AI",
    description=(
        "AI Comic Story Creator powered by Google Gemini Models "
        "and Stable Diffusion imagery."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

ensure_directories()
app.mount(
    "/static",
    StaticFiles(directory=str(settings.static_dir)),
    name="static",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "mock_mode": settings.mock_mode,
        "gemini_configured": bool(settings.gemini_api_key),
        "huggingface_configured": bool(settings.hf_token and not settings.hf_token.startswith("your_")),
        "outline_model": settings.gemini_outline_model,
        "story_model": settings.gemini_story_model,
        "image_model": settings.hf_image_model,
    }
