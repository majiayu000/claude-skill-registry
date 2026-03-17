---
name: openai-deep-research
description: Use OpenAI's Deep Research API (o3 / o4 models) to automate multi-step, citation-backed research workflows.
---

# OpenAI Deep Research Skill

This skill wraps OpenAI's Deep Research API so you can launch autonomous research runs (using `o3-deep-research` or `o4-mini-deep-research`) directly from Claude Code.

## Setup

1. **Dependencies:** Install the OpenAI SDK.

    ```bash
    pip install openai python-dotenv
    ```

2. **API Key Configuration:** Export your OpenAI API key.

    ```bash
    echo "OPENAI_API_KEY=sk-..." >> .env
    if [ -f .gitignore ] && ! grep -q ".env" .gitignore; then echo ".env" >> .gitignore; fi
    ```

    The Deep Research endpoint requires access to the Early Access program. Ensure your account is enabled before calling the API.

## Usage

Use `scripts/run_deep_research.py` to start a research job and stream the final report to stdout.

### Command

```bash
python3 scripts/run_deep_research.py --prompt "<research_question>" [--model o4-mini-deep-research] [--effort medium] [--json]
```

### Parameters

* `--prompt` (Required): The investigation prompt.
* `--model` (Optional): `o4-mini-deep-research` (default) or `o3-deep-research`.
* `--effort` (Optional): Reasoning depth, one of `low`, `medium`, `high` (default `medium`).
* `--json` (Optional): Emit the full response payload as JSON instead of just the synthesized report.
* `--output` (Optional): Write the report to a file path.

### Example

```bash
python3 scripts/run_deep_research.py \
  --prompt "Assess the projected market impact of solid state batteries by 2030" \
  --model o3-deep-research \
  --effort high \
  --output reports/solid-state-batteries.md
```

## Output

The script prints the synthesized Deep Research report (with citations) to stdout or saves it to the specified file. When `--json` is provided, the entire response payload (including intermediate steps, citations, and metadata) is emitted.

## Features

* **True Deep Research:** Uses OpenAI's autonomous planning, browsing, and synthesis stack.
* **Configurable Effort:** Choose between faster runs (`o4-mini-deep-research`) or higher-quality runs (`o3-deep-research`).
* **Intermediate Visibility:** Optional JSON output exposes the tool traces and citations returned by the API.
