import os
import uuid
from datetime import datetime
from pathlib import Path

from App.config import settings


def ensure_directories() -> None:
    """Ensure all required static and export directories exist."""
    settings.static_dir.mkdir(parents=True, exist_ok=True)
    settings.panels_dir.mkdir(parents=True, exist_ok=True)
    settings.exports_dir.mkdir(parents=True, exist_ok=True)
    (settings.static_dir / "css").mkdir(parents=True, exist_ok=True)
    (settings.static_dir / "js").mkdir(parents=True, exist_ok=True)
    (settings.static_dir / "images").mkdir(parents=True, exist_ok=True)


def new_comic_id() -> str:
    """Generate a clean timestamped unique identifier for a comic."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    short_hash = uuid.uuid4().hex[:6]
    return f"{timestamp}_{short_hash}"


def export_path(comic_id: str) -> Path:
    """Return the absolute filesystem path for the exported PDF."""
    return settings.exports_dir / f"comiccraft-{comic_id}.pdf"


def panel_image_path(comic_id: str, panel_number: int) -> Path:
    """Return the absolute filesystem path for a panel image."""
    return settings.panels_dir / f"{comic_id}_panel_{panel_number}.png"


def panel_image_url(comic_id: str, panel_number: int) -> str:
    """Return the web-accessible URL for a panel image."""
    return f"/static/panels/{comic_id}_panel_{panel_number}.png"

