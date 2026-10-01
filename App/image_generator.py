import io
import logging
import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

from App.config import settings
from App.storage import panel_image_path, panel_image_url

logger = logging.getLogger(__name__)


def _create_stylized_comic_art(
    prompt: str,
    comic_id: str,
    panel_number: int,
    width: int = 768,
    height: int = 512,
) -> Image.Image:
    """Generate a rich, colorful, stylized comic-book panel image using Pillow."""
    img = Image.new("RGB", (width, height), color=(20, 20, 30))
    draw = ImageDraw.Draw(img)

    # Curated comic color schemes per panel
    color_palettes = [
        # Panel 1: Dawn / Mystery (Deep Indigo to Golden Amber)
        ((18, 24, 58), (56, 32, 84), (235, 130, 60), (255, 215, 0)),
        # Panel 2: Glowing Discovery (Teal Cyan to Emerald & Magenta)
        ((10, 42, 54), (16, 92, 110), (28, 196, 178), (255, 90, 150)),
        # Panel 3: Dramatic Climax (Dark Crimson to Fiery Orange)
        ((48, 12, 24), (110, 22, 38), (220, 50, 40), (255, 170, 40)),
        # Panel 4: Energy Spark (Deep Violet to Electric Neon Blue & Cyan)
        ((25, 12, 55), (75, 25, 120), (120, 60, 230), (0, 230, 255)),
        # Panel 5: Triumphant Horizon (Sky Blue to Warm Rose & Sunset Gold)
        ((15, 30, 65), (45, 80, 140), (240, 110, 110), (255, 220, 120)),
        # Panel 6+: Neon Night
        ((15, 15, 35), (40, 30, 80), (180, 50, 180), (70, 210, 255)),
    ]

    palette_idx = (panel_number - 1) % len(color_palettes)
    c_dark, c_mid, c_bright, c_accent = color_palettes[palette_idx]

    # 1. Background vertical gradient
    for y in range(height):
        ratio = y / height
        if ratio < 0.5:
            sub_r = ratio / 0.5
            r = int(c_dark[0] + (c_mid[0] - c_dark[0]) * sub_r)
            g = int(c_dark[1] + (c_mid[1] - c_dark[1]) * sub_r)
            b = int(c_dark[2] + (c_mid[2] - c_dark[2]) * sub_r)
        else:
            sub_r = (ratio - 0.5) / 0.5
            r = int(c_mid[0] + (c_bright[0] - c_mid[0]) * sub_r)
            g = int(c_mid[1] + (c_bright[1] - c_mid[1]) * sub_r)
            b = int(c_mid[2] + (c_bright[2] - c_mid[2]) * sub_r)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # 2. Dynamic comic sunburst / action rays from focal center
    center_x = int(width * (0.4 + 0.2 * ((panel_number * 3) % 4) / 3))
    center_y = int(height * 0.45)
    num_rays = 28
    for i in range(num_rays):
        if i % 2 == 0:
            continue
        angle1 = (2 * math.pi / num_rays) * i
        angle2 = (2 * math.pi / num_rays) * (i + 0.8)
        radius = max(width, height) * 1.5
        p1 = (center_x, center_y)
        p2 = (center_x + radius * math.cos(angle1), center_y + radius * math.sin(angle1))
        p3 = (center_x + radius * math.cos(angle2), center_y + radius * math.sin(angle2))
        draw.polygon([p1, p2, p3], fill=(c_accent[0], c_accent[1], c_accent[2], 30))

    # 3. Glowing energy orbs / celestial aura in center
    for r in range(120, 20, -15):
        alpha = int(40 + (120 - r) * 1.2)
        draw.ellipse(
            [center_x - r, center_y - r, center_x + r, center_y + r],
            outline=c_accent,
            width=2,
        )

    # 4. Stylized dramatic silhouettes (mountains / cityscape / enchanted terrain)
    points_terrain = [(0, height)]
    for x in range(0, width + 40, 40):
        wave = math.sin(x * 0.015 + panel_number) * 45 + math.cos(x * 0.03) * 20
        y_pos = int(height * 0.68 + wave)
        points_terrain.append((x, y_pos))
    points_terrain.append((width, height))
    draw.polygon(points_terrain, fill=(12, 14, 25))

    # Second closer terrain layer
    points_foreground = [(0, height)]
    for x in range(0, width + 50, 50):
        wave2 = math.cos(x * 0.02 + panel_number * 1.5) * 30
        y_pos2 = int(height * 0.82 + wave2)
        points_foreground.append((x, y_pos2))
    points_foreground.append((width, height))
    draw.polygon(points_foreground, fill=(6, 8, 15))

    # 5. Stylized Heroic Character Silhouette
    char_x = int(width * 0.3)
    char_base_y = int(height * 0.80)
    # Head & shoulders
    draw.ellipse([char_x - 18, char_base_y - 95, char_x + 18, char_base_y - 60], fill=(245, 245, 250))
    # Glowing eyes / visor
    draw.line([(char_x - 6, char_base_y - 78), (char_x + 6, char_base_y - 78)], fill=c_accent, width=3)
    # Cape / torso
    draw.polygon(
        [
            (char_x - 14, char_base_y - 60),
            (char_x + 14, char_base_y - 60),
            (char_x + 35, char_base_y + 10),
            (char_x - 30, char_base_y + 10),
        ],
        fill=(15, 20, 35),
    )
    # Action aura outline around hero
    draw.ellipse([char_x - 40, char_base_y - 110, char_x + 40, char_base_y - 30], outline=c_accent, width=2)

    # 6. Comic Action Sound / Sparkle Sticker
    sound_effects = ["POW!", "WHOOSH!", "CRACKLE!", "GLOW!", "SHINE!", "ZAP!"]
    sfx = sound_effects[(panel_number - 1) % len(sound_effects)]
    sfx_x = width - 150
    sfx_y = 50

    # Draw comic blast shape for SFX
    blast_pts = []
    num_pts = 12
    for k in range(num_pts * 2):
        rad = 42 if k % 2 == 0 else 24
        ang = (math.pi / num_pts) * k
        blast_pts.append((sfx_x + rad * math.cos(ang), sfx_y + rad * math.sin(ang)))
    draw.polygon(blast_pts, fill=(255, 220, 0), outline=(20, 20, 20))
    draw.polygon([(x - 3, y - 3) for x, y in blast_pts], outline=(255, 255, 255))
    draw.text((sfx_x - 28, sfx_y - 8), sfx, fill=(20, 20, 20))

    # 7. Comic Panel Number Badge (Top Left)
    draw.rectangle([18, 18, 140, 52], fill=(15, 23, 42), outline=c_accent, width=2)
    draw.text((28, 26), f"PANEL #{panel_number}", fill=(255, 255, 255))

    # 8. Art Style & Prompt Ribbon (Bottom)
    draw.rectangle([0, height - 38, width, height], fill=(10, 15, 28, 220))
    draw.line([(0, height - 38), (width, height - 38)], fill=c_accent, width=2)
    display_prompt = prompt[:75] + ("..." if len(prompt) > 75 else "")
    draw.text((20, height - 28), f"PROMPT: {display_prompt}", fill=(200, 220, 255))

    # 9. Outer Comic Frame Border
    draw.rectangle([4, 4, width - 5, height - 5], outline=(255, 255, 255), width=3)
    draw.rectangle([8, 8, width - 9, height - 9], outline=(20, 20, 30), width=2)

    return img


def generate_image(
    prompt: str,
    comic_id: str,
    panel_number: int,
    art_style: str = "comic book",
    character_name: str = "",
    setting: str = "",
) -> str:
    """Generate a comic illustration via Hugging Face API or stylized fallback."""
    out_path = panel_image_path(comic_id, panel_number)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Enhance prompt with comic styling keywords
    enhanced_prompt = (
        f"{prompt}, {art_style} illustration, comic book art, vibrant colors, "
        f"detailed line art, dynamic lighting, masterpiece, 8k resolution"
    )

    hf_token = (settings.hf_token or "").strip()
    is_valid_hf_token = (
        bool(hf_token)
        and not hf_token.startswith("your_")
        and not hf_token.startswith("hf_placeholder")
    )

    if not settings.mock_mode and is_valid_hf_token:
        try:
            logger.info("Attempting Hugging Face image generation for panel %d...", panel_number)
            from huggingface_hub import InferenceClient

            client = InferenceClient(
                token=hf_token,
                provider=settings.hf_provider if settings.hf_provider != "auto" else None,
            )
            image = client.text_to_image(
                prompt=enhanced_prompt,
                model=settings.hf_image_model,
            )
            # Resize if needed
            image = image.resize((settings.image_width, settings.image_height))
            image.save(out_path, format="PNG")
            logger.info("HF image generation successful for panel %d", panel_number)
            return panel_image_url(comic_id, panel_number)
        except Exception as exc:
            logger.warning(
                "Hugging Face image generation failed (%s). Falling back to stylized comic art generator.",
                exc,
            )

    # Fallback / Mock Mode: Stylized high-res Pillow comic art
    comic_img = _create_stylized_comic_art(
        prompt=enhanced_prompt,
        comic_id=comic_id,
        panel_number=panel_number,
        width=settings.image_width,
        height=settings.image_height,
    )
    comic_img.save(out_path, format="PNG")
    return panel_image_url(comic_id, panel_number)

