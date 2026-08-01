# Gemini API Skill

> **Install:** `npx skills add diskd-ai/gemini-api` | [skills.sh](https://skills.sh)

Integration skill for building AI-powered applications with Google's Gemini API.

---

## Scope & Purpose

This skill provides guidance and patterns for working with Google's Gemini API, covering:

* Text generation with Gemini 3 and Gemini 2.5 models
* Multimodal inputs (image, video, audio, PDF)
* Image generation (Nano Banana)
* Video generation (Veo)
* Music generation (Lyria RealTime)
* Thinking/reasoning features
* Structured outputs with JSON schemas
* Function calling
* Embeddings

---

## When to Use This Skill

**Triggers:**
* Mentions of Gemini, Gemini 3, Gemini 2.5, or Google AI
* Using Python SDK (`google-genai`) or TypeScript SDK (`@google/genai`)
* Tasks involving Nano Banana, Veo, or Lyria
* Working with multimodal AI (images, video, audio, PDFs)

**Use cases:**
* Implementing text generation with Gemini models
* Processing documents and PDFs
* Generating images with Nano Banana
* Creating videos with Veo
* Generating music with Lyria RealTime
* Building agents with function calling
* Creating embeddings for RAG or semantic search

---

## Quick Reference

### Installation

```bash
# Python
pip install google-genai

# TypeScript/JavaScript
npm install @google/genai
```

### Environment

```bash
export GEMINI_API_KEY=<your-api-key>
```

### Basic Usage

**Python:**
```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="How does AI work?"
)
print(response.text)
```

**TypeScript:**
```typescript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: "How does AI work?",
});
console.log(response.text);
```

---

## Model Selection Guide

| Use Case | Model | Notes |
|----------|-------|-------|
| Fast + cheap | `gemini-3-flash-preview` | Best for simple tasks |
| Balanced | `gemini-2.5-flash` | Quality/cost balance |
| Highest quality | `gemini-3-pro-preview` | 1M context, thinking |
| Reasoning | `gemini-2.5-pro` | Deep thinking support |
| Vision | `gemini-3-flash-preview` | Image/video/audio/PDF |
| Image Gen | `gemini-2.5-flash-image` | Nano Banana |
| Image Gen Pro | `gemini-3-pro-image-preview` | Nano Banana Pro (4K) |
| Video Gen | `veo-3.1-generate-preview` | Video with audio |
| Music Gen | `lyria-realtime-exp` | Streaming music |
| Embeddings | `gemini-embedding-001` | Text embeddings |

---

## Skill Structure

```
gemini-api/
  SKILL.md          # Full API reference and patterns
  README.md         # This file (overview)
  references/       # Supporting documentation
    gemini-3.md     # Gemini 3 specific features
    thinking.md     # Thinking/reasoning guide
    image-generation.md  # Nano Banana patterns
    veo.md          # Video generation guide
    lyria.md        # Music generation guide
    function-calling.md  # Function calling patterns
    structured-outputs.md  # JSON schema outputs
    documents.md    # PDF processing
    embeddings.md   # Text embeddings
    tools.md        # Built-in tools
```

---

## Key Patterns

### Streaming Responses

```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Tell me a story"
):
    print(chunk.text, end="")
```

### Structured Outputs

```python
from pydantic import BaseModel

class Recipe(BaseModel):
    name: str
    ingredients: list[str]

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Extract: chocolate chip cookies need flour, sugar, chips",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)
```

### Multimodal (Image)

```python
from PIL import Image

image = Image.open("/path/to/image.png")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe this image"]
)
```

### Image Generation (Nano Banana)

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Create a picture of a sunset over mountains",
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("generated.png")
```

---

## Resources

* **Full skill reference**: [SKILL.md](SKILL.md)
* **Gemini 3 guide**: [references/gemini-3.md](references/gemini-3.md)
* **Thinking guide**: [references/thinking.md](references/thinking.md)
* **Image generation**: [references/image-generation.md](references/image-generation.md)
* **Video generation**: [references/veo.md](references/veo.md)
* **Music generation**: [references/lyria.md](references/lyria.md)
* **Function calling**: [references/function-calling.md](references/function-calling.md)
* **Official docs**: https://ai.google.dev/gemini-api/docs
* **Google AI Studio**: https://aistudio.google.com

---

## License

MIT
