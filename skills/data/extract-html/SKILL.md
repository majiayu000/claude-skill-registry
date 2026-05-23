---
name: extract-html
description: Extract structured JSON from HTML using Schematron3B, deterministic table extraction, and Vision-based media OCR.
triggers:
  - extract html
  - html to json
  - scrape html
  - table extraction
provides:
  - extract-html
composes:
  - task-monitor
---

# Extract-HTML Skill

A robust skill for converting HTML documents into strictly valid JSON based on a user-provided JSON Schema.

## Capabilities

1.  **Schema Compliance**: Guarantees output conforms to the provided JSON Schema (using Schematron-3B + validation loop).
2.  **Deterministic Tables**: Extracts HTML tables using `pandas.read_html` and injects them as context, preventing hallucination of data.
3.  **Media Text Extraction**: Identifies images, filters by pixel size, and optionally uses a Vision API (OpenAI-compatible) to extract text/OCR.
4.  **Self-Correction**: Validates model output and retries with error feedback if schema validation fails.

## Usage

### Basic Conversion (Local Only)

```bash
./run.sh convert \
  --html input.html \
  --schema target.schema.json \
  --out result.json
```

### Advanced (With Vision & Remote Fetch)

```bash
./run.sh convert \
  --html input.html \
  --schema target.schema.json \
  --out result.json \
  --fetch-remote-media \
  --vision-api-base "https://glhf.chat/api/openai/v1" \
  --vision-api-key "sk-..." \
  --vision-model "gpt-4o-mini"
```

## Options

- `--max-attempts <int>`: Number of self-correction retries.
- `--extract-tables / --no-extract-tables`: Toggle deterministic table extraction.
- `--extract-media-text`: Enable image processing.
- `--min-image-px`, `--max-image-px`: Filter images by size.
- `--include-sections`: detailed H1-H6 hierarchy in context.

## Dependencies

- Ollama running `schematron-3b` (or compatible model).
- Python 3.11+
- See `pyproject.toml` for python deps.
