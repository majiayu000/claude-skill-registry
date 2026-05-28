---
name: gemini-gen
description: Generates images using Google's Gemini model. Prioritizes standard resolution to save quota. Automatically opens images on macOS.
---

# Gemini Image Generator

This skill generates images using Google's Gemini model. It is configured to be cost-efficient by defaulting to standard resolution models.

## Usage

```bash
python3 {script_path} "Prompt" [--model model_name] [--output filename.png] [--no-open]
```

## IMPORTANT: Model Selection Policy (Quota Saving)
**Always default to standard resolution models.** Do NOT use 4K models unless the user explicitly mentions "4K", "Ultra HD", or "High Definition".

### Available Models

| Model Name | Aspect Ratio | Resolution | Cost Category |
| :--- | :--- | :--- | :--- |
| **`gemini-3-pro-image` (Default)** | 1:1 | Standard | **Low (Recommended)** |
| `gemini-3-pro-image-16x9` | 16:9 | Standard | **Low (Recommended)** |
| `gemini-3-pro-image-9x16` | 9:16 | Standard | **Low (Recommended)** |
| `gemini-3-pro-image-4k` | 1:1 | 4K | High |
| `gemini-3-pro-image-4k-16x9` | 16:9 | 4K | High |
| `gemini-3-pro-image-4k-9x16` | 9:16 | 4K | High |

## Decision Logic for Alma
1. **Default**: Use `gemini-3-pro-image`.
2. **Aspect Ratio**: 
   - If "landscape/widescreen/16:9", use `gemini-3-pro-image-16x9`.
   - If "portrait/mobile/9:16", use `gemini-3-pro-image-9x16`.
3. **4K (Only if explicitly requested)**:
   - Only upgrade to a `-4k` model if the user explicitly says "4K" or equivalent high-res keywords.

### Note on Display
Alma's chat UI does not render local images. The skill uses `open` to show the image in the system viewer.
