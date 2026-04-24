---
name: smolvlm
description: Local vision-language model for image analysis using SmolVLM-2B
version: 1.0.0
---

# SmolVLM - Local Image Analysis

Analyze images locally using SmolVLM-2B, a state-of-the-art compact vision-language model optimized for Apple Silicon via mlx-vlm.

## Quick Usage

### Describe an Image
```bash
python ~/.claude/skills/smolvlm/scripts/view_image.py /path/to/image.png
```

### Ask a Question About an Image
```bash
python ~/.claude/skills/smolvlm/scripts/view_image.py /path/to/image.png "What text is visible?"
```

### Specific Tasks
```bash
# Extract text (OCR)
python ~/.claude/skills/smolvlm/scripts/view_image.py screenshot.png "Extract all text"

# UI analysis
python ~/.claude/skills/smolvlm/scripts/view_image.py ui.png "Describe the UI elements"

# Detailed description
python ~/.claude/skills/smolvlm/scripts/view_image.py photo.jpg --detailed
```

## Effective Prompts

### General Description
- `"Describe this image"` - Basic description
- `"Describe this image in detail, including colors, composition, and any text"` - Comprehensive

### Text Extraction (OCR)
- `"Extract all visible text from this image"`
- `"What text appears in this screenshot?"`
- `"Read the text in this document"`

### UI/Screenshot Analysis
- `"Describe the user interface elements"`
- `"What buttons and controls are visible?"`
- `"Identify the application and its current state"`

### Visual Question Answering
- `"How many [objects] are in this image?"`
- `"What color is the [object]?"`
- `"Is there a [object] in this image?"`

### Code/Technical
- `"What programming language is shown?"`
- `"Describe what this code does"`
- `"Identify any errors in this code screenshot"`

## Model Details

| Spec | Value |
|------|-------|
| Model | SmolVLM-2B-Instruct |
| Size | ~4GB |
| Peak Memory | 5.8GB |
| Speed | ~94 tok/s (M-series) |
| Supported Formats | PNG, JPG, JPEG, GIF, WebP |

## Requirements

- macOS with Apple Silicon (M1/M2/M3)
- Python 3.10+
- mlx-vlm package: `uv pip install mlx-vlm --system`

## Troubleshooting

**"Model not found"**: First run downloads the model (~4GB). Wait for completion.

**Out of memory**: Close other applications. Model needs ~6GB free RAM.

**Slow first inference**: Model loading takes 10-15s on first use, subsequent calls are faster.
