---
name: vision-language-models
description: GPT-5/4o, Claude 4.5, Gemini 2.5/3, Grok 4 vision patterns for image analysis, document understanding, and visual QA. Use when implementing image captioning, document/chart analysis, or multi-image comparison.
context: fork
agent: multimodal-specialist
version: 1.0.0
author: SkillForge
user-invocable: false
tags: [vision, multimodal, image, gpt-5, claude-4, gemini, grok, vlm, 2026]
---

# Vision Language Models (2026)

Integrate vision capabilities from leading multimodal models for image understanding, document analysis, and visual reasoning.

## When to Use

- Image captioning and description generation
- Visual question answering (VQA)
- Document/chart/diagram analysis with OCR
- Multi-image comparison and reasoning
- Bounding box detection and region analysis
- Video frame analysis

## Model Comparison (January 2026)

| Model | Context | Strengths | Vision Input |
|-------|---------|-----------|--------------|
| **GPT-5.2** | 128K | Best general reasoning, multimodal | Up to 10 images |
| **Claude Opus 4.5** | 200K | Best coding, sustained agent tasks | Up to 100 images |
| **Gemini 2.5 Pro** | 1M+ | Longest context, video analysis | 3,600 images max |
| **Gemini 3 Pro** | 1M | Deep Think, 100% AIME 2025 | Enhanced segmentation |
| **Grok 4** | 2M | Real-time X integration, DeepSearch | Images + upcoming video |

## Image Input Methods

### Base64 Encoding (All Providers)

```python
import base64
import mimetypes

def encode_image_base64(image_path: str) -> tuple[str, str]:
    """Encode local image to base64 with MIME type."""
    mime_type, _ = mimetypes.guess_type(image_path)
    mime_type = mime_type or "image/png"

    with open(image_path, "rb") as f:
        base64_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return base64_data, mime_type
```

### OpenAI GPT-5/4o Vision

```python
from openai import OpenAI

client = OpenAI()

def analyze_image_openai(image_path: str, prompt: str) -> str:
    """Analyze image using GPT-5 or GPT-4o."""
    base64_data, mime_type = encode_image_base64(image_path)

    response = client.chat.completions.create(
        model="gpt-5",  # or "gpt-4o", "gpt-4.1"
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:{mime_type};base64,{base64_data}",
                    "detail": "high"  # low, high, or auto
                }}
            ]
        }],
        max_tokens=4096  # Required for vision
    )
    return response.choices[0].message.content
```

### Claude 4.5 Vision (Anthropic)

```python
import anthropic

client = anthropic.Anthropic()

def analyze_image_claude(image_path: str, prompt: str) -> str:
    """Analyze image using Claude Opus 4.5 or Sonnet 4.5."""
    base64_data, media_type = encode_image_base64(image_path)

    response = client.messages.create(
        model="claude-opus-4-5-20251124",  # or claude-sonnet-4-5
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": base64_data
                    }
                },
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.content[0].text
```

### Gemini 2.5/3 Vision (Google)

```python
import google.generativeai as genai
from PIL import Image

genai.configure(api_key="YOUR_API_KEY")

def analyze_image_gemini(image_path: str, prompt: str) -> str:
    """Analyze image using Gemini 2.5 Pro or Gemini 3."""
    model = genai.GenerativeModel("gemini-2.5-pro")  # or gemini-3-pro

    image = Image.open(image_path)

    response = model.generate_content([prompt, image])
    return response.text

# For video analysis (Gemini excels here)
def analyze_video_gemini(video_path: str, prompt: str) -> str:
    """Analyze video using Gemini's native video support."""
    model = genai.GenerativeModel("gemini-2.5-pro")

    video_file = genai.upload_file(video_path)

    response = model.generate_content([prompt, video_file])
    return response.text
```

### Grok 4 Vision (xAI)

```python
from openai import OpenAI  # Grok uses OpenAI-compatible API

client = OpenAI(
    api_key="YOUR_XAI_API_KEY",
    base_url="https://api.x.ai/v1"
)

def analyze_image_grok(image_path: str, prompt: str) -> str:
    """Analyze image using Grok 4 with real-time capabilities."""
    base64_data, mime_type = encode_image_base64(image_path)

    response = client.chat.completions.create(
        model="grok-4",  # or grok-2-vision-1212
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:{mime_type};base64,{base64_data}"
                }}
            ]
        }]
    )
    return response.choices[0].message.content
```

## Multi-Image Analysis

```python
async def compare_images(images: list[str], prompt: str) -> str:
    """Compare multiple images (Claude supports up to 100)."""
    content = []

    for img_path in images:
        base64_data, media_type = encode_image_base64(img_path)
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": base64_data
            }
        })

    content.append({"type": "text", "text": prompt})

    response = client.messages.create(
        model="claude-opus-4-5-20251124",
        max_tokens=8192,
        messages=[{"role": "user", "content": content}]
    )
    return response.content[0].text
```

## Object Detection (Gemini 2.5+)

```python
def detect_objects_gemini(image_path: str) -> list[dict]:
    """Detect objects with bounding boxes using Gemini 2.5+."""
    model = genai.GenerativeModel("gemini-2.5-pro")
    image = Image.open(image_path)

    response = model.generate_content([
        "Detect all objects in this image. Return bounding boxes "
        "as JSON with format: {objects: [{label, box: [x1,y1,x2,y2]}]}",
        image
    ])

    import json
    return json.loads(response.text)
```

## Token Cost Optimization

| Provider | Detail Level | Cost Impact |
|----------|-------------|-------------|
| OpenAI | `low` (65 tokens) | Use for classification |
| OpenAI | `high` (129+ tokens/tile) | Use for OCR/charts |
| Gemini | 258 tokens base | Scales with resolution |
| Claude | Per-image pricing | Batch for efficiency |

```python
# Cost-optimized simple classification
response = client.chat.completions.create(
    model="gpt-4o-mini",  # Cheaper for simple tasks
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Is there a person? Reply: yes/no"},
            {"type": "image_url", "image_url": {
                "url": image_url,
                "detail": "low"  # Minimal tokens
            }}
        ]
    }]
)
```

## Image Size Limits (2026)

| Provider | Max Size | Max Images | Notes |
|----------|----------|------------|-------|
| OpenAI | 20MB | 10/request | GPT-5 series |
| Claude | 8000x8000 px | 100/request | 2000px if >20 images |
| Gemini | 20MB | 3,600/request | Best for batch |
| Grok | 20MB | Limited | Grok 5 expands this |

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| High accuracy | Claude Opus 4.5 or GPT-5 |
| Long documents | Gemini 2.5 Pro (1M context) |
| Cost efficiency | Gemini 2.5 Flash ($0.15/M tokens) |
| Real-time/X data | Grok 4 with DeepSearch |
| Video analysis | Gemini 2.5/3 Pro (native) |

## Common Mistakes

- Not setting `max_tokens` (responses truncated)
- Sending oversized images (resize to 2048px max)
- Using `high` detail for yes/no questions
- Not validating image format before encoding
- Ignoring rate limits on vision endpoints
- Using deprecated models (GPT-4V retired)

## Limitations

- Cannot identify specific people (privacy restriction)
- May hallucinate on low-quality/rotated images (<200px)
- GPT-4o: struggles with non-Latin text, precise spatial reasoning
- No real-time video (use frame extraction except Gemini)

## Related Skills

- `audio-language-models` - Audio/speech processing
- `multimodal-rag` - Image + text retrieval
- `llm-streaming` - Streaming vision responses

## Capability Details

### image-captioning
**Keywords:** caption, describe, image description, alt text, accessibility
**Solves:**
- Generate descriptive captions for images
- Create accessibility alt text
- Extract visual content summary

### visual-qa
**Keywords:** VQA, visual question, image question, analyze image
**Solves:**
- Answer questions about image content
- Extract specific information from visuals
- Reason about image elements

### document-vision
**Keywords:** document, PDF, chart, diagram, OCR, extract, table
**Solves:**
- Extract text from documents and charts
- Analyze diagrams and flowcharts
- Process forms and tables with structure

### multi-image-analysis
**Keywords:** compare images, multiple images, image comparison, batch
**Solves:**
- Compare visual elements across images
- Track changes between versions
- Analyze image sequences

### object-detection
**Keywords:** bounding box, detect objects, locate, segmentation
**Solves:**
- Detect and locate objects in images
- Generate bounding box coordinates
- Segment image regions (Gemini 2.5+)
