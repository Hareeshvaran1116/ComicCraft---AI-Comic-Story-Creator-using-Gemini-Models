import logging
from pathlib import Path

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)
from fastapi.responses import (
    FileResponse,
    HTMLResponse,
)
from fastapi.templating import Jinja2Templates

from App.config import settings
from App.exporters import save_pdf
from App.image_generator import generate_image
from App.layout_builder import build_comic_layout
from App.mock_ai import mock_outline, mock_story
from App.schemas import (
    ComicLayout,
    PromptRequest,
)
from App.storage import (
    export_path,
    new_comic_id,
)

logger = logging.getLogger(__name__)

router = APIRouter()

# Resolve templates directory (check both templates and Templates)
_tmpl_dir = settings.templates_dir
if not _tmpl_dir.exists():
    alt_tmpl = settings.base_dir / "Templates"
    if alt_tmpl.exists():
        _tmpl_dir = alt_tmpl

templates = Jinja2Templates(directory=str(_tmpl_dir))


def run_generation(request_data: PromptRequest) -> ComicLayout:
    """Execute the end-to-end comic generation pipeline."""
    comic_id = new_comic_id()

    # Step 1: Generate Comic Outline
    if settings.mock_mode:
        outline = mock_outline(request_data)
        story = mock_story(request_data, outline)
    else:
        from App.gemini_flash import generate_outline
        from App.gemini_pro import generate_story

        outline = generate_outline(request_data)
        story = generate_story(request_data, outline)

    # Step 2: Generate Illustrations for each panel
    image_urls = []
    for panel in outline.panels:
        img_url = generate_image(
            prompt=panel.image_prompt,
            comic_id=comic_id,
            panel_number=panel.panel_number,
            art_style=request_data.art_style,
            character_name=request_data.character_name,
            setting=request_data.setting,
        )
        image_urls.append(img_url)

    # Step 3: Organize Layout
    panels = build_comic_layout(
        outline=outline,
        story=story,
        image_urls=image_urls,
        comic_id=comic_id,
    )

    # Step 4: Export to PDF
    pdf_url = save_pdf(
        comic_id=comic_id,
        panels=panels,
        story_title=outline.story_title,
        character_name=request_data.character_name,
        setting_name=request_data.setting,
        tone=request_data.tone,
        art_style=request_data.art_style,
    )

    return ComicLayout(
        comic_id=comic_id,
        story_title=outline.story_title,
        character_name=request_data.character_name,
        setting=request_data.setting,
        tone=request_data.tone,
        art_style=request_data.art_style,
        panels=panels,
        pdf_url=pdf_url,
    )


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Render the ComicCraft creator studio homepage."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"settings": settings},
    )


@router.post("/generate", response_class=HTMLResponse)
def generate_comic_form(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(...),
    setting: str = Form(...),
    tone: str = Form("light-hearted"),
    art_style: str = Form("comic book"),
    panels: int = Form(5),
):
    """Handle web form submission and display generated comic preview."""
    try:
        payload = PromptRequest(
            story_prompt=story_prompt.strip(),
            character_name=character_name.strip(),
            setting=setting.strip(),
            tone=tone.strip(),
            art_style=art_style.strip(),
            panels=panels,
        )

        comic = run_generation(payload)

        return templates.TemplateResponse(
            request=request,
            name="comic_preview.html",
            context={
                "comic": comic,
                "settings": settings,
            },
        )

    except Exception as exc:
        logger.exception("Comic generation failed: %s", exc)
        return templates.TemplateResponse(
            request=request,
            name="error.html",
            context={
                "message": f"Unable to generate comic: {str(exc)}",
                "settings": settings,
            },
            status_code=500,
        )


@router.post("/generate-comic/json", response_model=ComicLayout)
def generate_comic_json(payload: PromptRequest):
    """REST API endpoint to generate comic via JSON payload."""
    try:
        return run_generation(payload)
    except Exception as exc:
        logger.exception("JSON comic generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail=f"Comic generation error: {str(exc)}",
        ) from exc


@router.post("/test-image")
def test_image(prompt: str = Form(...)):
    """Developer utility route to test image generation for a single prompt."""
    try:
        comic_id = new_comic_id()
        image_url = generate_image(
            prompt=prompt,
            comic_id=comic_id,
            panel_number=1,
            art_style="comic book",
        )
        return {"status": "ok", "image_url": image_url}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/download/{comic_id}")
def download_pdf(comic_id: str):
    """Download the generated PDF comic book."""
    path = export_path(comic_id)
    if not path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Comic PDF for ID '{comic_id}' not found.",
        )

    return FileResponse(
        path=str(path),
        media_type="application/pdf",
        filename=f"ComicCraft-{comic_id}.pdf",
    )


@router.get("/export-success", response_class=HTMLResponse)
def export_success(request: Request, comic_id: str | None = None):
    """Render the comic export confirmation and download page."""
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={
            "comic_id": comic_id,
            "settings": settings,
        },
    )
