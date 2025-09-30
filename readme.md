# MorningMotivationBot

A tiny Flask web app that gives you a personalized morning motivation message (with a tone you pick), a matching YouTube song, and a peaceful image. It uses:

- **OpenAI API** (chat + images via the new `openai` SDK v1)
- **TextBlob** for quick sentiment analysis
- **python-dotenv** to load secrets from a local `.env` file
- A simple HTML form with a loading spinner and a clean CSS style

---

## Features

- Detects your mood from free‑text using TextBlob and tunes the system prompt accordingly.
- Generates a motivational message + haiku + 3 actionable steps.
- Extracts a **YouTube video link** (the model supplies it) and renders it.
- Generates a peaceful **image** using OpenAI’s image generation.
- Simple, single‑file Flask backend (`app.py`) + `templates/index.html` + `static/style.css`.

---

## Project Structure

```
MotivationBot/
├─ app.py
├─ templates/
│  └─ index.html
├─ static/
│  └─ style.css
├─ .env                 # (DO NOT COMMIT) your local secrets live here
├─ .env.example         # template you DO commit
├─ requirements.txt     # pinned dependencies
└─ .gitignore
```

> If you don’t have `requirements.txt` yet, see **Freeze dependencies** below.

---

## Prerequisites

- **Python 3.10+** recommended (your current setup shows 3.13.7 and works).
- An **OpenAI API key** with access to the chat and image endpoints.

---

## 1) Set up your environment variables

Create a `.env` file in the project root (same folder as `app.py`) by copying the example:
```bash
cp .env.example .env
```

Open `.env` and fill in your key:
```
OPENAI_API_KEY=sk-...your_key_here...
```
**Important notes**
- No quotes around the value.
- No spaces around `=`.
- Keep `.env` **out of git** (it’s in `.gitignore`).

If you’re using a **project key** (`sk-proj-...`) and your org/project enforces scoping, ensure your key is valid for your default org/project. If you hit `401 invalid_api_key`, see **Troubleshooting**.

---

## 2) Create and activate a virtual environment

### macOS / Linux (bash/zsh)
```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
```

### Windows (PowerShell)
```powershell
py -m venv venv
venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

---

## 3) Install dependencies

If you already have `requirements.txt` (recommended):
```bash
pip install -r requirements.txt
```

If you don’t, start by installing what the app needs:
```bash
pip install Flask openai python-dotenv textblob
```
> Optional (rarely needed): if TextBlob ever complains about corpora, run:
> ```bash
> python -m textblob.download_corpora
> ```

Then **freeze** the exact versions:

```bash
pip freeze > requirements.txt
```

Commit `requirements.txt` so anyone can reproduce your environment:
```bash
git add requirements.txt
git commit -m "Add pinned requirements"
```

---

## 4) Run the app

From the project root (with your venv active and `.env` set up):

```bash
# Option A: flask cli
flask run

# Option B: run directly
python app.py
```

By default the app runs at: http://127.0.0.1:5000/

---

## How it works (quick tour)

- `app.py`
  - Loads `.env` via `load_dotenv()` and creates an OpenAI client:
    ```python
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    ```
  - Uses `TextBlob` to estimate sentiment polarity and selects a “mood” system message.
  - Calls `client.chat.completions.create(...)` (model: `gpt-4o`) to generate the motivation text.
  - Extracts a YouTube URL (if present) and pulls out its video id for display.
  - Calls `client.images.generate(...)` (model: `dall-e-3`) for a calming image URL.
  - Renders everything in `templates/index.html`.

- `templates/index.html`
  - Simple form (feeling + tone), submit shows a spinner, then displays response, song, image.

- `static/style.css`
  - Minimal, friendly gradient UI with responsive text.

