---
name: ppt-translator
description: Translate PowerPoint presentations while preserving formatting (fonts, colors, alignment, tables). Supports multiple LLM providers (OpenAI, Anthropic, DeepSeek, Grok, Gemini). Use when translating .pptx files between languages, especially for CJK to/from English translations where text expansion/contraction is a concern.
license: MIT - see LICENSE.txt
---

# PowerPoint Translation Skill

Translate PowerPoint presentations while preserving all formatting including fonts, colors, spacing, tables, and alignment.

## When to Use This Skill

- Translating `.pptx` files between languages
- Batch translating multiple presentations in a directory
- Preserving slide formatting during translation (especially CJK ↔ English)
- When you need to inspect intermediate XML for debugging

## Setup

Before first use, set up the environment:

```bash
# Navigate to the scripts directory
cd .claude/skills/ppt-translator/scripts

# Create virtual environment and install dependencies
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt

# Configure API keys
cp example.env .env
# Edit .env with your provider API key(s)
```

## Basic Usage

```bash
cd .claude/skills/ppt-translator/scripts
source .venv/bin/activate

python main.py /path/to/presentation.pptx \
  --provider openai \
  --source-lang zh \
  --target-lang en
```

## Provider Configuration

| Provider  | Environment Variable | Default Model              |
|-----------|---------------------|----------------------------|
| openai    | `OPENAI_API_KEY`    | `gpt-5.2-2025-12-11`       |
| anthropic | `ANTHROPIC_API_KEY` | `claude-sonnet-4-5-20250514` |
| deepseek  | `DEEPSEEK_API_KEY`  | `deepseek-chat`            |
| grok      | `GROK_API_KEY`      | `grok-4.1-fast`            |
| gemini    | `GEMINI_API_KEY`    | `gemini-3-flash-preview`   |

## CLI Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--provider` | LLM provider: `openai`, `anthropic`, `deepseek`, `grok`, `gemini` | `openai` |
| `--model` | Override default model for provider | Provider default |
| `--source-lang` | Source language ISO code | `zh` |
| `--target-lang` | Target language ISO code | `en` |
| `--max-chunk-size` | Characters per API request | `1000` |
| `--max-workers` | Threads for slide extraction | `4` |
| `--keep-intermediate` | Retain XML files for debugging | `false` |

## Output Files

For each input `presentation.pptx`, the tool generates:

1. `presentation_original.xml` - Extracted source content (deleted unless `--keep-intermediate`)
2. `presentation_translated.xml` - Translated content (deleted unless `--keep-intermediate`)
3. `presentation_translated.pptx` - Final translated presentation with formatting intact

## Common Workflows

### Translate a Single File (Chinese → English)

```bash
python main.py deck.pptx --provider anthropic --source-lang zh --target-lang en
```

### Batch Translate a Directory

```bash
python main.py /path/to/presentations/ --provider openai --source-lang ja --target-lang en
```

### Debug Translation Issues

```bash
python main.py deck.pptx --keep-intermediate --provider deepseek
# Inspect the generated XML files to see extracted/translated content
```

### Use a Specific Model

```bash
python main.py deck.pptx --provider openai --model gpt-5-mini
```

### Translate with Gemini (Cost-Effective)

```bash
python main.py deck.pptx --provider gemini --source-lang ko --target-lang en
```

## Supported Languages

Use standard ISO 639-1 language codes:

| Code | Language |
|------|----------|
| `zh` | Chinese (Simplified) |
| `en` | English |
| `ja` | Japanese |
| `ko` | Korean |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `pt` | Portuguese |
| `ru` | Russian |
| `ar` | Arabic |

## Design Notes

### Font Scaling

The tool automatically scales fonts down (70% for text, 80% for tables) to accommodate text expansion when translating from compact languages (Chinese, Japanese, Korean) to English. This prevents text overflow in fixed-size text boxes.

### Caching

Repeated strings within a presentation are cached to avoid redundant API calls. This is especially useful for presentations with recurring headers, footers, or terminology.

### Chunking

Long text blocks are intelligently split at sentence boundaries to stay within API limits while preserving translation quality.

## Troubleshooting

### "API key not found"

Ensure your `.env` file in the scripts directory contains the correct environment variable:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

### Formatting looks wrong

1. Use `--keep-intermediate` to inspect the XML files
2. Check if the source presentation has unusual formatting
3. Try a different provider

### Translation incomplete

1. Check for API rate limits with your provider
2. Try reducing `--max-chunk-size` for very long text blocks
3. Ensure your API key has sufficient quota

## Script Reference

The `scripts/` directory contains:

- `main.py` - Entry point
- `requirements.txt` - Python dependencies
- `example.env` - Environment variable template
- `ppt_translator/` - Core translation module
  - `cli.py` - CLI argument parsing
  - `pipeline.py` - PPT extraction and regeneration
  - `translation.py` - Chunking and caching
  - `providers/` - LLM provider implementations
