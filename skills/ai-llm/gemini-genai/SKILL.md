---
name: gemini-genai
description: Google python-genai SDK for Gemini 3 Flash, Gemini 3 Pro, and Gemini models. Use when building with Google's Gemini API, google-genai, implementing thinking/reasoning, structured outputs, function calling, image generation, or multimodal. Triggers on "gemini", "google ai", "genai".
---

# Google Gemini python-genai SDK

## Model IDs

| Model | ID |
|-------|-----|
| Gemini 3 Flash | `gemini-3-flash-preview` |
| Gemini 3 Pro | `gemini-3-pro-preview` |
| Gemini 3 Pro Image | `gemini-3-pro-image-preview` |
| Gemini 2.5 Flash | `gemini-2.5-flash` |
| Gemini 2.5 Pro | `gemini-2.5-pro` |

## Gemini 3 Flash Capabilities

**Token Limits**: 1,048,576 input / 65,536 output (confirmed 1M context)

**Inputs**: Text, Image, Video, Audio, PDF

**Supported**: Batch API, Caching, Code execution, File search, Function calling, Search grounding, Structured outputs, Thinking, URL context

**Not Supported**: Audio generation, Image generation (use gemini-3-pro-image-preview), Live API, Grounding with Google Maps

**Knowledge cutoff**: January 2025

## Critical: Temperature for Gemini 3

**Keep `temperature=1.0`** - Lower values cause response looping.

## Thinking Levels (Gemini 3)

```python
config=types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(thinking_level="high")  # minimal|low|medium|high
)
```
- `minimal`: No thinking, lowest latency (Flash only)
- `high`: Maximum reasoning (default)

## Async Pattern

```python
async with genai.Client().aio as client:
    response = await client.models.generate_content(...)

# Async chat
chat = client.aio.chats.create(model="gemini-3-flash-preview")
```

## Media Resolution (v1alpha required)

```python
client = genai.Client(http_options=types.HttpOptions(api_version='v1alpha'))

types.Part(
    inline_data=types.Blob(mime_type="image/jpeg", data=image_bytes),
    media_resolution={"level": "media_resolution_high"}  # low|medium|high|ultra_high
)
```
Tokens: low=280, medium=560, high=1120

## Built-in Tools (Gemini 3)

```python
config=types.GenerateContentConfig(
    tools=[{"google_search": {}}],    # Web search
    # tools=[{"url_context": {}}],    # Fetch URL content
    # tools=[{"code_execution": {}}], # Run code
)
```

## Enum Response

```python
from enum import Enum

class Category(Enum):
    A = "A"
    B = "B"

config={
    "response_mime_type": "text/x.enum",
    "response_schema": Category,
}
```

## Image Generation

```python
response = client.models.generate_content(
    model="gemini-3-pro-image-preview",
    contents="A cyberpunk city",
    config=types.GenerateContentConfig(
        response_modalities=["IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9", image_size="4K"),
    ),
)
image = response.parts[0].as_image()
image.save("out.png")
```

Grounded (with search): Add `tools=[{"google_search": {}}]`

## Response Helpers

```python
response.text           # Text content
response.parsed         # Auto-parsed JSON (when using response_json_schema)
response.function_calls # List of function calls (cleaner than candidates drilling)
```

## Pricing (Gemini 3 Flash)

Input: $0.50/1M | Output: $3.00/1M | Context caching: up to 90% reduction

## Resources

- GitHub: https://github.com/googleapis/python-genai
- Docs: https://googleapis.github.io/python-genai/
