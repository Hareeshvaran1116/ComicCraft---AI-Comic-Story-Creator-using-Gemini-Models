# 💥 ComicCraft AI — AI Comic Story Creator

> **Generative AI Comic Story Studio using Google Gemini Models & Stable Diffusion**

---

## 📖 Overview

**ComicCraft AI** is an intelligent web application that transforms user story prompts into multi-panel comic strips complete with vivid storyline outlines, immersive captions, character dialogues, and high-quality illustrations. 

The application integrates:
- **Google Gemini Flash (`gemini-1.5-flash`)** for rapid, structured multi-panel story outlines and image generation prompts.
- **Google Gemini Pro (`gemini-1.5-pro`)** for writing rich narration, ambient captions, and dynamic character dialogue.
- **Stable Diffusion / Hugging Face Diffusion Models** (with high-resolution stylized rendering fallback) for generating comic panel artwork.
- **FPDF2 PDF Engine** for compiling the comic story, metadata, artwork, and narrative into a professional downloadable PDF document.
- **FastAPI Backend & Jinja2 Modern UI** for smooth browser interactions and REST API endpoints.

---

## 🌟 Key Features

1. **🎨 Interactive Story Creator Studio**:
   - Customizable story prompt, character name, setting, tone (*light-hearted, dramatic, funny, poetic*), and art style (*comic book, anime, pixel art, realistic*).
   - One-click prompt presets (*Brave Fox, Cyberpunk Detective, Space Explorer, Dragon Academy*).
   - Dynamic real-time loading overlay tracking each AI generation stage.

2. **⚡ Multi-Model AI Story Generation**:
   - 5-panel coherent narrative arc with title, scene descriptions, and specialized visual prompts.
   - Panel-by-panel captions, action narrations, and character dialogues formatted in comic speech bubbles.

3. **🖼️ Comic Panel Artwork Generation**:
   - Powered by Hugging Face `InferenceClient` (Stable Diffusion) with rich artistic canvas rendering fallback ensuring 100% reliable previews.

4. **📄 Multi-Page PDF Comic Book Export**:
   - Generates a styled comic booklet with cover page, metadata card, panel artwork, captions, and speech boxes.
   - Dedicated download endpoint (`/download/{comic_id}`) and export confirmation page (`/export-success`).

5. **🔌 Full REST API Integration**:
   - Interactive Swagger API docs at `/docs`.
   - Programmatic JSON comic generation at `/generate-comic/json`.
   - Single prompt image testing endpoint at `/test-image`.
   - Health status endpoint at `/health`.

---

## 🏗️ Project Architecture & Structure

```
ComicCraftAI/
├── .env                       # Environment variables (Gemini API key, HF token, models)
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
├── app/                       # Application source code
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization & static mounts
│   ├── routes.py              # Route handlers for web UI & REST API
│   ├── config.py              # Pydantic settings & env management
│   ├── schemas.py             # Pydantic data models (PromptRequest, ComicLayout, etc.)
│   ├── storage.py             # Directory management & path resolvers
│   ├── gemini_flash.py        # Gemini Flash 5-panel outline generator
│   ├── gemini_pro.py          # Gemini Pro dialogue & narrative generator
│   ├── image_generator.py     # Stable Diffusion & artistic comic image engine
│   ├── layout_builder.py      # Combines outline, story & art into panel layouts
│   ├── exporters.py           # Multi-page PDF generation via FPDF2
│   ├── mock_ai.py             # Dynamic mock generators for offline testing
│   └── ai/                    # AI integration sub-package
├── templates/                 # Jinja2 HTML templates
│   ├── base.html              # Base layout with navbar, footer & styling
│   ├── index.html             # Homepage creation studio & prompt presets
│   ├── comic_preview.html     # Sequential comic panel viewer & PDF download
│   ├── export_success.html    # Export confirmation page
│   └── error.html             # Error handling page
└── static/                    # Static assets & generated outputs
    ├── css/
    │   └── style.css          # Modern comic studio CSS design system
    ├── panels/                # Generated panel images
    └── exports/               # Exported PDF comic books
```

---

## 🚀 Quickstart & Setup Guide

### 1. Prerequisites
- **Python 3.10+** installed
- Optional: Google Gemini API Key and Hugging Face Token

### 2. Create and Activate Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (`.env`)

Configure your `.env` file in the project root:

```ini
# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_OUTLINE_MODEL=gemini-1.5-flash
GEMINI_STORY_MODEL=gemini-1.5-pro

# Hugging Face Token & Model
HF_TOKEN=your_huggingface_token_here
HF_IMAGE_MODEL=stabilityai/stable-diffusion-3.5-large-turbo
HF_PROVIDER=auto

# Settings
MOCK_MODE=false
PANELS=5
IMAGE_WIDTH=768
IMAGE_HEIGHT=512
```

> **Note**: If `MOCK_MODE=true` or if API keys are not provided, ComicCraft automatically uses the built-in dynamic mock AI engine and stylized art generator so the entire application runs smoothly out of the box!

### 5. Launch the FastAPI Development Server

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open your browser and navigate to:
- 🌐 **Web Studio UI**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- 📚 **Interactive Swagger API**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- 🩺 **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web Comic Studio Homepage |
| `POST` | `/generate` | Web form submission to generate & preview comic |
| `POST` | `/generate-comic/json` | REST API endpoint accepting `PromptRequest` JSON |
| `POST` | `/test-image` | Developer utility to test single-prompt image generation |
| `GET` | `/download/{comic_id}` | Download generated PDF comic book |
| `GET` | `/export-success` | Comic export confirmation page |
| `GET` | `/health` | Service status and AI configuration check |

---

## 🧪 Example API Request (cURL)

```bash
curl -X POST "http://127.0.0.1:8000/generate-comic/json" \
  -H "Content-Type: application/json" \
  -d '{
    "story_prompt": "A young brave fox exploring an enchanted forest finds a glowing crystal",
    "character_name": "Nova",
    "setting": "Enchanted Whispering Forest",
    "tone": "light-hearted",
    "art_style": "comic book",
    "panels": 5
  }'
```

---

## 📄 License & Credits
Built for AI Comic Creation using Google Gemini models, Hugging Face Diffusers, and FastAPI.
