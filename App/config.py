from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Gemini settings
    gemini_api_key: str = ""
    gemini_outline_model: str = "gemini-1.5-flash"
    gemini_story_model: str = "gemini-1.5-pro"

    # Hugging Face / Image Generation settings
    hf_token: str = ""
    hf_image_model: str = "stabilityai/stable-diffusion-3.5-large-turbo"
    hf_provider: str = "auto"

    # Application settings
    mock_mode: bool = False
    panels: int = 5
    image_width: int = 768
    image_height: int = 512

    # Paths
    base_dir: Path = Path(__file__).resolve().parent.parent
    static_dir: Path = base_dir / "static"
    templates_dir: Path = base_dir / "templates"
    panels_dir: Path = static_dir / "panels"
    exports_dir: Path = static_dir / "exports"


settings = Settings()

