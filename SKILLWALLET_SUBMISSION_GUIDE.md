# 📘 ComicCraft AI — SkillWallet Project Submission & Team Guide

---

## 👥 1. Team Role & Task Allocation (5 Team Members)

As Team Lead, you can assign the milestones and activities to your 5 team members on SkillWallet as follows:

| Member | Role | Assigned Milestone & Activities | Key Files & Responsibilities |
| :--- | :--- | :--- | :--- |
| **Member 1 (You - Team Lead)** | **System Architect & Backend Lead** | **Milestone 1 & Milestone 5**<br>• Activity 1.1: Model Selection & Architecture<br>• Activity 1.2: App Architecture Definition<br>• Activity 5.1 & 5.2: Environment Setup, `.env` & Deployment | `app/config.py`, `app/main.py`, `.env`, `run.bat`, `run.py` |
| **Member 2** | **AI Storytelling & Outline Engineer** | **Milestone 2 (Part 1)**<br>• Activity 2.1: Gemini Flash 5-Panel Outline Generation | `app/gemini_flash.py`, `app/ai/gemini_flash.py`, `app/schemas.py` |
| **Member 3** | **Dialogue & Narration Specialist** | **Milestone 2 (Part 2)**<br>• Activity 2.1: Gemini Pro Story Narration & Character Dialogue | `app/gemini_pro.py`, `app/ai/gemini_pro.py`, `app/mock_ai.py` |
| **Member 4** | **Image Generation & PDF Export Engineer** | **Milestone 2 (Part 3)**<br>• Activity 2.1: Stable Diffusion Artwork & FPDF2 PDF Exporter | `app/image_generator.py`, `app/layout_builder.py`, `app/exporters.py`, `app/storage.py` |
| **Member 5** | **Frontend UI/UX Developer** | **Milestone 3 & Milestone 4**<br>• Activity 3.1: FastAPI `routes.py` Integration<br>• Activity 4.1 & 4.2: Jinja2 Dynamic Templates & CSS Styling | `app/routes.py`, `templates/index.html`, `templates/comic_preview.html`, `templates/export_success.html`, `static/css/style.css` |

---

## 📋 2. Milestone-by-Milestone SkillWallet Answers

### 🔹 Milestone 1: Model Selection and Architecture
- **Activity 1.1: Research and Select the Appropriate Generative AI Model**
  - **Models Selected**:
    1. **Google Gemini Flash (`gemini-1.5-flash`)**: High speed and structured JSON output for 5-panel comic outlines, panel titles, scene descriptions, and image prompts.
    2. **Google Gemini Pro (`gemini-1.5-pro`)**: Deep creative writing capabilities for engaging character dialogues, ambient sound captions, and narrations.
    3. **Stable Diffusion (`runwayml/stable-diffusion-v1-5` / Hugging Face)**: High-resolution visual comic art generation matching panel descriptions.
- **Activity 1.2: Define Application Architecture**
  - **Frontend**: HTML5, Vanilla CSS3 (Comic Dark Theme), Jinja2 Templates.
  - **Backend**: FastAPI with Uvicorn ASGI server.
  - **AI Layer**: Google GenAI SDK (`google-genai`), Hugging Face Diffusers / Inference API, and Canvas fallback.
  - **Export Layer**: `fpdf2` for compiling multi-page comic books.
- **Activity 1.3: Set up Development Environment**
  - Installed libraries: `fastapi`, `uvicorn`, `jinja2`, `python-multipart`, `google-genai`, `fpdf2`, `Pillow`, `huggingface-hub`.

---

### 🔹 Milestone 2: Core Functionalities Development
- **Activity 2.1: Develop Core Modules**
  1. `app/gemini_flash.py` -> `generate_outline(request)`: Creates 5 sequential panel outlines.
  2. `app/gemini_pro.py` -> `generate_story(request, outline)`: Writes dialogues and narrations.
  3. `app/image_generator.py` -> `generate_image(prompt, comic_id, panel_number)`: Generates comic panel art.
  4. `app/layout_builder.py` -> `build_comic_layout()`: Maps text, dialogues, and images into structured panel cards.
  5. `app/exporters.py` -> `save_pdf()`: Builds the cover page, metadata, and multi-page PDF booklet.
- **Activity 2.2: Implement FastAPI Backend & Route Processing**
  - Connected input forms (`index.html`) and JSON API requests (`PromptRequest`) to backend pipelines.

---

### 🔹 Milestone 3: routes.py Development
- **Activity 3.1: Main Application Logic in `app/routes.py`**
  - `GET /`: Serves the ComicCraft Creator Studio homepage.
  - `POST /generate`: Form submission endpoint processing AI generation and rendering `comic_preview.html`.
  - `POST /generate-comic/json`: REST API endpoint returning full `ComicLayout` JSON.
  - `POST /test-image`: Utility route to test image prompts.
  - `GET /download/{comic_id}`: PDF download endpoint.
  - `GET /export-success`: Export confirmation screen.
  - `GET /health`: Health and AI configuration status.

---

### 🔹 Milestone 4: Frontend Development
- **Activity 4.1: UI Design & Responsive Layout**
  - Designed comic book aesthetics in `static/css/style.css` using Google Fonts (*Bangers*, *Outfit*, *Inter*), dark glassmorphism cards, and halftone textures.
- **Activity 4.2: Dynamic Jinja2 Templates**
  - `base.html`: Common navigation bar, footer, and texture.
  - `index.html`: Story prompt presets (*Brave Fox, Cyberpunk Detective, Space Explorer, Dragon Academy*) and multi-step loading animation.
  - `comic_preview.html`: Panel-by-panel viewer with speech bubbles, italic scene descriptions, narration boxes, and PDF download button.
  - `export_success.html`: Download confirmation page.

---

### 🔹 Milestone 5: Deployment
- **Activity 5.1: Local Environment Configuration**
  - Configured environment variables in `.env` (`GEMINI_API_KEY`, `HF_TOKEN`, models).
- **Activity 5.2: Verification and Server Startup**
  - Ran server with `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`.
  - Verified UI at `http://127.0.0.1:8000` and Swagger docs at `http://127.0.0.1:8000/docs`.

---

## 🎯 3. Simple Viva / Interview Questions & Answers

1. **Q: What is the main objective of ComicCraft AI?**
   - **A**: To allow non-artists and storytellers to transform simple story prompts into complete, multi-panel comic strips with dialogues, artwork, and exportable PDF comic books using generative AI.

2. **Q: Why use two different Gemini models (Flash and Pro)?**
   - **A**: **Gemini 1.5 Flash** is fast, lightweight, and ideal for generating structured JSON 5-panel outlines and image prompts. **Gemini 1.5 Pro** has stronger creative nuance for rich narration and character dialogues.

3. **Q: How does the PDF generation work?**
   - **A**: We use the `fpdf2` library in `app/exporters.py` to programmatically assemble a cover page, character metadata, panel images, and dialogue bubbles into a downloadable multi-page PDF document.

4. **Q: What happens if there is no internet or an API key expires?**
   - **A**: The system features a built-in `mock_ai.py` engine and Pillow-based comic canvas generator that dynamically creates stylized comic panels and stories so the application never crashes.
