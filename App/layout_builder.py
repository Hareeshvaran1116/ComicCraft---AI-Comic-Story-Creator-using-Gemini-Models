from typing import List
from App.schemas import ComicOutline, ComicPanel, ComicStory


def build_comic_layout(
    outline: ComicOutline,
    story: ComicStory,
    image_urls: List[str],
    comic_id: str,
) -> List[ComicPanel]:
    """Assemble panel outlines, written stories, and generated images into structured comic panels."""
    panels: List[ComicPanel] = []

    # Map story parts by panel_number for fast lookup
    story_map = {s.panel_number: s for s in story.panels}

    for i, p_outline in enumerate(outline.panels):
        p_num = p_outline.panel_number
        p_story = story_map.get(p_num)

        img_url = image_urls[i] if i < len(image_urls) else f"/static/panels/{comic_id}_panel_{p_num}.png"

        caption = p_story.caption if p_story else f"Panel {p_num}"
        narration = p_story.narration if p_story else p_outline.scene_description
        dialogue = p_story.dialogue if p_story else ""

        panel = ComicPanel(
            panel_number=p_num,
            title=p_outline.title,
            image_url=img_url,
            scene_description=p_outline.scene_description,
            caption=caption,
            narration=narration,
            dialogue=dialogue,
            image_prompt=p_outline.image_prompt,
        )
        panels.append(panel)

    return panels

