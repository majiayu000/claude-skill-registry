---
name: sketch-ai-provider-debug
description: Debug OpenAI/Gemini image generation failures for Sketch Magic. Use when `/api/convert` returns 500, when models are unsupported, when outputs are empty, or when provider timeouts/quota errors appear.
---

# Sketch AI Provider Debug

## Overview
Provide a consistent debug flow for image generation failures across OpenAI and Gemini providers without leaking secrets.

## Workflow

### 1) Verify configuration
- Confirm `OPENAI_API_KEY` / `GEMINI_API_KEY` exist.
- Confirm `DEFAULT_PROVIDER`, `OPENAI_IMAGE_MODEL`, `GEMINI_IMAGE_MODEL` match supported models.
- Use `/api/health` to confirm defaults.

### 2) Reproduce with a controlled request
- Use a tiny PNG and short prompt.
- Use `curl` to hit `/api/convert` (multipart form data).
- Keep logs visible (server + client).

### 3) Interpret common failures
- **500**: provider error, missing key, quota, or model mismatch.
- **400**: invalid image type, size, or prompt.
- **Timeout**: provider latency or host timeout config.

### 4) Fix or adjust
- Swap to a known-good model.
- Reduce image size or prompt complexity.
- Confirm provider SDK versions align with supported endpoints.

### 5) Report safely
- Do not log API keys or raw image bytes.
- Summarize error codes and timing only.

## References
- `references/openai-image-api.md`
- `references/gemini-image-api.md`
