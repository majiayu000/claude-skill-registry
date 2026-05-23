---
name: jina-ai
description: Use Jina AI APIs for converting URLs to LLM-friendly Markdown (Reader) and searching the web (Search).
---

# Jina AI Skill

This skill integrates Jina AI's Reader (r.jina.ai) and Search (s.jina.ai) APIs to convert URLs and web search results into clean, LLM-friendly Markdown.

## Setup

1. **Dependencies:** Requires `requests`.

    ```bash
    pip install requests python-dotenv
    ```

2. **API Key Configuration (Recommended):** Jina APIs offer higher limits with an API key (JINA_API_KEY).

    ```bash
    read -p "Enter your Jina API key (optional, press Enter to skip): " JINA_KEY
    if [ ! -z "$JINA_KEY" ]; then
        echo "JINA_API_KEY=$JINA_KEY" >> .env
        if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
        echo "API key saved to .env."
    fi
    ```

## Usage

The script `scripts/jina_tools.py` supports `read` and `search` operations.

### 1. Read URL (Jina Reader)

Convert a URL into clean Markdown.

```bash
python3 scripts/jina_tools.py read "<url>"
```

**Example:**

```bash
python3 scripts/jina_tools.py read "https://en.wikipedia.org/wiki/Large_language_model"
```

### 2. Search Web (Jina Search)

Search the web and return the top results converted to Markdown.

```bash
python3 scripts/jina_tools.py search "<query>"
```

**Example:**

```bash
python3 scripts/jina_tools.py search "What is Jina AI?"
```

## Output

The script outputs results in JSON format, containing title, URL, and `content_markdown`.
