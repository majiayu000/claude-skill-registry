---
name: gemini-image-gen
description: Image generation with Google Gemini API. Models: gemini-2.5-flash-image (fast) or gemini-3-pro-image-preview (quality). For social media graphics, marketing, infographics.
---

# Gemini Image Generation

Generate images directly from Claude Code CLI using Google's Gemini API.

## Setup

**API Key:** https://aistudio.google.com/apikey
**Environment Variable:** `GOOGLE_AI_API_KEY`
**Install:** `pip install google-genai pillow python-dotenv`

## Basic Usage

```python
import os
from google import genai

client = genai.Client(api_key=os.environ.get("GOOGLE_AI_API_KEY"))

response = client.models.generate_content(
    model="gemini-2.5-flash-image",  # Fast
    # model="gemini-3-pro-image-preview",  # Quality
    contents=["Your image prompt here"]
)

# Extract and save image from response
for part in response.candidates[0].content.parts:
    if hasattr(part, 'inline_data') and part.inline_data:
        with open("output.png", "wb") as f:
            f.write(part.inline_data.data)
```

## Models

| Model | Speed | Quality | Use Case |
|-------|-------|---------|----------|
| `gemini-2.5-flash-image` | Fast (~5s) | Good | Drafts, iterations |
| `gemini-3-pro-image-preview` | Slower (~15s) | Excellent | Final assets |

## Use Cases

- Social media graphics
- Marketing materials
- Infographics
- Reddit/Discord banners
- Presentation slides
- Manufacturing dashboards (OEE gauges, SPC charts)

## Advanced: Manufacturing Dashboard Example

```python
prompt = """
Create a professional manufacturing OEE dashboard showing:
- Large OEE gauge at 85% (green zone)
- Three smaller KPI cards below:
  - Availability: 92%
  - Performance: 88%
  - Quality: 99.2%
- Dark theme with blue/cyan accents
- Modern, executive-style design
"""

response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents=[prompt]
)
```

## Image Compression for PPTX

When embedding in PowerPoint, compress images to avoid silent failures:

```python
from PIL import Image
import io

def compress_image(data: bytes, max_size_kb: int = 200) -> bytes:
    img = Image.open(io.BytesIO(data))
    img = img.convert('RGB')
    img.thumbnail((1280, 720))

    buffer = io.BytesIO()
    img.save(buffer, format='JPEG', quality=75, optimize=True)
    return buffer.getvalue()
```

## Real-World Usage

At [fabrikIQ.com](https://www.fabrikiq.com), Gemini Image Generation powers:
- AI-generated OEE dashboard visuals in PPTX exports
- Hero images for executive manufacturing reports
- Marketing materials for LinkedIn posts
