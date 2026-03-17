---
name: scillm
description: >
  Managed scillm Paved Path execution.
  Provides strict contract-compliant tools for Text Batch, VLM, and Lean4 Proving.
  Uses `parallel_acompletions_iter` for reliable large-scale processing.
allowed-tools: Bash, Read
triggers:
  - batch LLM calls
  - parallel completions
  - describe image
  - prove mathematically
  - extract JSON
metadata:
  short-description: Scillm Paved Path (Text, VLM, Proofs)
---

# Scillm Paved Path Skill

This skill provides **contract-compliant** wrappers around `scillm` for robust agent operations.
It enforces the patterns defined in `SCILLM_PAVED_PATH_CONTRACT.md`.

## Features

- **Strict `uv run` Execution**: No global environment dependencies (outside of `uv`).
- **Parallel Iterators**: Uses `parallel_acompletions_iter` for fault-tolerant batch processing.
- **Multimodal Standards**: Correctly formats VLM payloads.
- **VLM Inputs**: Accepts file paths, HTTPS URLs, or `data:` URIs; `--inline-remote-images` (or `SCILLM_INLINE_REMOTE_IMAGES=1`) downloads remote assets before dispatch, and `--dry-run` previews payloads without live calls.
- **Preflight Helpers**: `run.sh preflight ...` shells into `scillm.paved.sanity_preflight` and `list_models_openai_like` for Step 07 readiness checks.
- **JSON Strict by Default**: `--json` automatically enables `SCILLM_JSON_STRICT`, with optional `--schema`, `--retry-invalid-json`, and repair flags.

## Usage Guide

### 1. Text Batch Processing (`batch.py`)

Use for large-scale text extraction or summarization.

**Command:**

```bash
.pi/skills/scillm/run.sh batch --input prompts.jsonl --output results.jsonl --json
```

**Input Format (JSONL):**

```json
{"prompt": "Summarize this article..."}
{"prompt": "Extract names from...", "id": "123"}
```

**Code Pattern (Python):**
The skill implements this Paved Path pattern:

```python
from scillm.batch import parallel_acompletions_iter

reqs = [
    {"model": "model-id", "messages": [{"role": "user", "content": "prompt"}]}
]

async for res in parallel_acompletions_iter(reqs, concurrency=6):
    if res["ok"]:
        print(res["content"])
```

### 2. VLM / Multimodal (`vlm.py`)

Use for describing images, diagrams, or Tables.

**Command:**

```bash
.pi/skills/scillm/run.sh vlm describe image.png --prompt "Extract table data" --json
```

- Supports `--inline-remote-images` (with optional `--inline-remote-timeout`) to download HTTPS assets when the gateway cannot reach them, and `--dry-run` to print the payload without making an API call (used by sanity scripts).

**Batch Command:**

```bash
.pi/skills/scillm/run.sh vlm batch --input images.jsonl
```

**Code Pattern (Python):**
The skill enforces the correct VLM message structure:

```python
messages = [{
    "role": "user",
    "content": [
        {"type": "text", "text": "Describe this..."},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}
    ]
}]
await acompletion(..., messages=messages)
```

### 3. Lean4 Proving (`prove.py`)

Use for formal verification steps.

**Command:**

```bash
.pi/skills/scillm/run.sh prove "Prove that n + 0 = n"
```

### 4. Preflight + Model Discovery (`preflight.py`)

Use to run paved-step `sanity_preflight` and list models without bespoke scripts.

**Commands:**

```bash
# Model availability + auth style
.pi/skills/scillm/run.sh preflight preflight --model "$CHUTES_MODEL_ID" --json

# List models (returns JSON array)
.pi/skills/scillm/run.sh preflight models --json
```

These commands exit non-zero when the model is unavailable, making them CI-friendly.

---

## Infrastructure

- **Entry Point**: `run.sh` (dispatches via `uv run`)
- **Dependencies**: Defined in `pyproject.toml` (`scillm`, `typer`)
- **Verification**: `sanity.sh` verifies CLI help and structural integrity.
