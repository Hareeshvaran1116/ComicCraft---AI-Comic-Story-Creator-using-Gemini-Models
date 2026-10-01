from typing import List, Optional
from pydantic import BaseModel, Field


class PromptRequest(BaseModel):
    story_prompt: str = Field(..., description="Main story concept or plot prompt")
    character_name: str = Field(..., description="Main protagonist name")
    setting: str = Field(..., description="Story setting or location")
    tone: str = Field(default="light-hearted", description="Mood or tone of the comic")
    art_style: str = Field(default="comic book", description="Visual art style")
    panels: int = Field(default=5, ge=3, le=8, description="Number of panels to generate")


class ComicPanelOutline(BaseModel):
    panel_number: int = Field(..., description="Sequential panel number, starting from 1")
    title: str = Field(..., description="Short catchy title for this panel")
    scene_description: str = Field(..., description="Atmosphere, mood, and brief scene context")
    image_prompt: str = Field(..., description="Detailed AI image generation prompt")


class ComicOutline(BaseModel):
    story_title: str = Field(default="ComicCraft Story", description="Overall comic story title")
    summary: str = Field(default="", description="High-level narrative summary")
    panels: List[ComicPanelOutline] = Field(default_factory=list, description="List of panel outlines")


class PanelStory(BaseModel):
    panel_number: int = Field(..., description="Panel number corresponding to the outline")
    caption: str = Field(default="", description="Ambient scene caption or sound effect description")
    narration: str = Field(default="", description="Action narration and story movement")
    dialogue: str = Field(default="", description="Character speech, dialogue or thoughts")


class ComicStory(BaseModel):
    story_title: Optional[str] = None
    panels: List[PanelStory] = Field(default_factory=list, description="List of panel stories")


class ComicPanel(BaseModel):
    panel_number: int
    title: str
    image_url: str
    scene_description: str
    caption: str
    narration: str
    dialogue: str
    image_prompt: str


class ComicLayout(BaseModel):
    comic_id: str
    story_title: str = "ComicCraft Comic"
    character_name: str = ""
    setting: str = ""
    tone: str = ""
    art_style: str = ""
    panels: List[ComicPanel] = Field(default_factory=list)
    pdf_url: str = ""

