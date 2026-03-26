---
name: modal-labs
description: Modal Labs (modal.com) — run Python on serverless containers with GPUs, batch jobs, and autoscaling. Precision wrapper to avoid confusion with UI “modal dialogs”.
license: Apache-2.0 license
metadata:
  skill-author: Local wrapper (VCO)
  upstream-skill: modal
  routing-notes: Prefer this skill over `modal` for auto-routing; reserve `modal` for explicit calls to avoid UI ambiguity.
---

# Modal Labs (modal.com)

## Overview

This is a **precision wrapper** for the upstream `modal` skill (Modal Labs, modal.com). It exists because “modal” is also a common term for UI dialogs (React/Vue/AntD/etc.).  

Use this skill only when the user clearly means **Modal Labs (modal.com)**.

## When to Use

Route here when prompts mention one or more of:
- `modal.com` / “Modal Labs”
- CLI verbs: `modal run`, `modal deploy`, `modal serve`
- serverless containers for Python, **batch jobs**, autoscaling
- **GPU** workloads (inference, training, rendering) in a serverless setup

Do **not** use this skill for UI “modal dialog” tasks.

## Setup (CLI)

```bash
# Install
uv uv pip install modal

# Login (writes token to ~/.modal.toml)
modal token new
```

## Minimal Example

```python
import modal

app = modal.App("hello-modal")

@app.function()
def hello():
    return "hello from Modal"

@app.local_entrypoint()
def main():
    print(hello.remote())
```

Run:

```bash
modal run script.py
```

## Next Actions (choose based on intent)

- **One-off run:** `modal run`
- **Long-running endpoint:** `modal deploy` / `modal serve`
- **GPU function:** add `@app.function(gpu="H100")` (or another GPU type)

If you need deeper patterns (images, volumes, secrets, web endpoints), follow the upstream `modal` skill guidance.
