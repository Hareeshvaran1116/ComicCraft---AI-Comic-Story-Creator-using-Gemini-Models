from App.schemas import (
    ComicOutline,
    ComicPanelOutline,
    ComicStory,
    PanelStory,
    PromptRequest,
)


def mock_outline(request: PromptRequest) -> ComicOutline:
    """Generate a dynamic, high-quality mock comic outline based on user input."""
    char = request.character_name or "The Hero"
    setting = request.setting or "The Mysterious Realm"
    tone = request.tone or "light-hearted"
    style = request.art_style or "comic book"
    prompt_snippet = request.story_prompt[:60] if request.story_prompt else "The Great Adventure"

    story_title = f"{char}'s Quest: {prompt_snippet.strip().capitalize()}"

    panel_templates = [
        (
            f"The Awakening in {setting}",
            f"{char} stands at the dawn of a new journey in {setting}, noticing unusual signs in the environment.",
            f"{style} style illustration of {char} standing in {setting} at golden dawn, dramatic cinematic lighting, wide establishing shot, high detail",
        ),
        (
            "An Unexpected Discovery",
            f"While investigating deeper into {setting}, {char} stumbles upon an ancient artifact humming with energy.",
            f"{style} style vibrant close-up of {char} reaching towards a glowing magical artifact in {setting}, colorful particle effects, dynamic perspective",
        ),
        (
            "The Looming Challenge",
            f"A sudden rumbling echoes across {setting} as an obstacle challenges {char}'s resolve in a {tone} turn of events.",
            f"{style} dynamic action scene of {char} facing a dramatic obstacle in {setting}, bold outlines, intense atmosphere, high contrast shadows",
        ),
        (
            "Unleashing the Spark",
            f"Gathering courage, {char} uses cleverness and the discovered power to turn the tide in {setting}.",
            f"{style} superhero comic climax shot of {char} unleashing a burst of vibrant energy in {setting}, radiant neon highlights, comic action lines",
        ),
        (
            "A New Dawn",
            f"With victory achieved, {char} gazes across {setting}, having grown stronger and ready for what lies ahead.",
            f"{style} triumphant ending shot of {char} smiling at the horizon over {setting}, warm twilight glow, cinematic widescreen frame",
        ),
        (
            "The Legend Begins",
            f"Word of {char}'s deeds spreads across {setting}, inspiring everyone who hears the tale.",
            f"{style} inspiring celebratory scene of {char} celebrated by allies in {setting}, festive atmosphere, rich vibrant colors",
        ),
        (
            "Secrets in the Shadows",
            f"In the quiet corners of {setting}, a hint of an even greater mystery is revealed for {char}.",
            f"{style} intriguing mystery teaser shot showing {char} gazing at a glowing map in {setting}, atmospheric moonlit illumination",
        ),
        (
            "To the Next Horizon",
            f"{char} packs their gear and steps forward onto the path of endless future adventures.",
            f"{style} epic journey continuation scene of {char} walking along a winding path beyond {setting}, heroic silhouette against sunset",
        ),
    ]

    panels = []
    num_panels = min(max(request.panels, 3), 8)

    for i in range(num_panels):
        idx = i if i < len(panel_templates) else i % len(panel_templates)
        title, scene, img_prompt = panel_templates[idx]
        panels.append(
            ComicPanelOutline(
                panel_number=i + 1,
                title=f"Panel {i + 1}: {title}",
                scene_description=scene,
                image_prompt=img_prompt,
            )
        )

    return ComicOutline(
        story_title=story_title,
        summary=f"A {tone} story featuring {char} navigating the wonders and trials of {setting}.",
        panels=panels,
    )


def mock_story(request: PromptRequest, outline: ComicOutline) -> ComicStory:
    """Generate dynamic narrative captions and dialogues matching the outline."""
    char = request.character_name or "The Hero"
    setting = request.setting or "The Realm"
    tone = request.tone.lower()

    dialogue_flavors = {
        "funny": [
            f'"{char}: Well, this certainly wasn\'t in the brochure!"',
            f'"{char}: If this explodes, I\'m blaming the map."',
            f'"{char}: On a scale of one to ten, we are at maximum oops."',
            f'"{char}: Ta-da! And you thought I didn\'t have a plan!"',
            f'"{char}: All in a day\'s work... now where\'s the snack bar?"',
        ],
        "dramatic": [
            f'"{char}: The winds of {setting} have changed. It begins now."',
            f'"{char}: This power... it has been waiting for centuries."',
            f'"{char}: Stand firm! No matter what emerges from the shadows!"',
            f'"{char}: With every ounce of strength I possessâ€”break!"',
            f'"{char}: Peace returns to {setting}, but our vigil never ends."',
        ],
        "poetic": [
            f'"{char}: Whispers of wind through {setting} carry forgotten songs."',
            f'"{char}: Light dances upon the edge of discovery."',
            f'"{char}: When darkness gathers, the heart becomes a flame."',
            f'"{char}: In one fleeting moment, destiny was rewritten."',
            f'"{char}: The horizon opens wide, painted in hues of tomorrow."',
        ],
        "light-hearted": [
            f'"{char}: Another beautiful day in {setting}! Let\'s see what we find."',
            f'"{char}: Whoa, look at that glow! This might just be our lucky day."',
            f'"{char}: Time to put our skills to the test!"',
            f'"{char}: We did it! Never doubted ourselves for a second!"',
            f'"{char}: Ready for the next adventure whenever you are!"',
        ],
    }

    selected_dialogues = dialogue_flavors.get(tone, dialogue_flavors["light-hearted"])

    panel_stories = []
    for i, panel in enumerate(outline.panels):
        dlg = (
            selected_dialogues[i % len(selected_dialogues)]
            if selected_dialogues
            else f'"{char}: Onward!"'
        )

        caption_text = f"Chapter {i + 1} â€¢ {panel.title.replace(f'Panel {i+1}: ', '')}"
        narration_text = (
            f"As {char} moved across {setting}, {panel.scene_description.lower()}"
        )

        panel_stories.append(
            PanelStory(
                panel_number=panel.panel_number,
                caption=caption_text,
                narration=narration_text,
                dialogue=dlg,
            )
        )

    return ComicStory(
        story_title=outline.story_title,
        panels=panel_stories,
    )

