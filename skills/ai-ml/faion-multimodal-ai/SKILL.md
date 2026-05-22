---
name: faion-multimodal-ai
description: "Multimodal AI: vision, image/video generation, speech-to-text, text-to-speech, voice synthesis."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task, AskUserQuestion, TodoWrite
---
> **Entry point:** `/faion-net` — invoke this skill for automatic routing to the appropriate domain.

# Multimodal AI Skill

**Communication: User's language. Code: English.**

## Purpose

Handles multimodal AI applications. Covers vision, image generation, video generation, speech, and voice synthesis.

## Context Discovery

### Auto-Investigation

Check these project signals before asking questions:

| Signal | Where to Check | What to Look For |
|--------|----------------|------------------|
| **Dependencies** | package.json, requirements.txt | openai, PIL/pillow, ffmpeg-python, elevenlabs |
| **Media files** | /images, /audio, /video | Input files to process |
| **API usage** | Grep for "images.generate", "audio.transcriptions" | Existing multimodal APIs |
| **Output dirs** | /generated, /output | Where generated content goes |

### Discovery Questions

```yaml
question: "Which modality are you working with?"
header: "Modality"
multiSelect: true
options:
  - label: "Vision (image understanding)"
    description: "GPT-4o Vision, Gemini Vision for OCR/analysis"
  - label: "Image generation"
    description: "DALL-E 3, Midjourney, Stable Diffusion"
  - label: "Video generation/understanding"
    description: "Sora, Runway, or video analysis"
  - label: "Speech-to-text"
    description: "Whisper, Deepgram for transcription"
  - label: "Text-to-speech"
    description: "OpenAI TTS, ElevenLabs for voice synthesis"
```

```yaml
question: "What's your primary use case?"
header: "Use Case"
multiSelect: false
options:
  - label: "Document/receipt OCR and analysis"
    description: "Extract structured data from images"
  - label: "Content generation (images/videos)"
    description: "Create marketing/creative assets"
  - label: "Accessibility (vision/speech conversion)"
    description: "Convert between modalities for a11y"
  - label: "Voice assistant/bot"
    description: "Speech → Text → LLM → TTS pipeline"
```

```yaml
question: "Volume and latency requirements?"
header: "Scale"
multiSelect: false
options:
  - label: "Low volume, quality over speed"
    description: "Use premium models (HD TTS, GPT-4o Vision)"
  - label: "High volume, optimize for cost"
    description: "Batch APIs, smaller models"
  - label: "Real-time required"
    description: "Streaming APIs (Deepgram, OpenAI TTS)"
  - label: "Async processing OK"
    description: "Queue-based approach"
```

## Scope

| Area | Coverage |
|------|----------|
| **Vision** | GPT-4o Vision, Gemini Vision, image understanding |
| **Image Generation** | DALL-E 3, Midjourney, Stable Diffusion |
| **Video Generation** | Sora, Runway, Pika |
| **Speech-to-Text** | Whisper, Deepgram, AssemblyAI |
| **Text-to-Speech** | OpenAI TTS, ElevenLabs, Google TTS |
| **Voice** | Real-time voice, voice cloning |

## Quick Start

| Task | Files |
|------|-------|
| Vision API | vision-basics.md → vision-applications.md |
| Image generation | img-gen-basics.md → img-gen-tools.md |
| Video generation | video-gen-basics.md → video-gen-tools.md |
| Speech-to-text | speech-to-text-basics.md → speech-to-text-advanced.md |
| Text-to-speech | tts-basics.md → tts-implementation.md |
| Voice synthesis | voice-basics.md → voice-implementation.md |

## Methodologies (12)

**Vision (2):**
- vision-basics: Image understanding, OCR, scene analysis
- vision-applications: Use cases, production patterns

**Image Generation (2):**
- img-gen-basics: Prompt engineering, models
- img-gen-tools: DALL-E 3, Midjourney, Stable Diffusion

**Video Generation (2):**
- video-gen-basics: Fundamentals, prompting
- video-gen-tools: Sora, Runway, Pika, Luma

**Speech-to-Text (2):**
- speech-to-text-basics: Whisper API, real-time
- speech-to-text-advanced: Diarization, timestamps

**Text-to-Speech (2):**
- tts-basics: Voice selection, SSML
- tts-implementation: Production patterns, streaming

**Voice (2):**
- voice-basics: Real-time voice, cloning
- voice-implementation: Integration patterns

## Code Examples

### GPT-4o Vision

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {"type": "image_url", "image_url": {"url": "https://..."}}
        ]
    }]
)
```

### DALL-E 3 Image Generation

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A futuristic city with flying cars",
    size="1024x1024",
    quality="hd",
    n=1
)

image_url = response.data[0].url
```

### Whisper Speech-to-Text

```python
from openai import OpenAI

client = OpenAI()

audio_file = open("speech.mp3", "rb")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word"]
)

print(transcription.text)
```

### OpenAI TTS

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="alloy",
    input="Hello, this is a test of text to speech."
)

response.stream_to_file("speech.mp3")
```

### Gemini Vision

```python
import google.generativeai as genai

genai.configure(api_key="...")
model = genai.GenerativeModel('gemini-pro-vision')

image = PIL.Image.open("image.jpg")
response = model.generate_content([
    "Describe this image in detail",
    image
])

print(response.text)
```

## Model Comparison

### Vision Models

| Model | Best For | Max Image Size |
|-------|----------|----------------|
| GPT-4o | General vision, OCR | 20MB |
| Gemini Pro Vision | High-res images | 20MB |
| Claude Sonnet 4 | Document analysis | 5MB |

### Image Generation

| Model | Best For | Cost |
|-------|----------|------|
| DALL-E 3 | Photorealistic, text | $$$ |
| Midjourney | Artistic, creative | $$ |
| Stable Diffusion | Custom, open-source | Free/$ |

### Speech-to-Text

| Service | Best For | Languages |
|---------|----------|-----------|
| Whisper | General, multilingual | 99 |
| Deepgram | Real-time, low latency | 30+ |
| AssemblyAI | Features, diarization | 10+ |

### Text-to-Speech

| Service | Best For | Voices |
|---------|----------|--------|
| OpenAI TTS | Quality, variety | 6 |
| ElevenLabs | Cloning, realism | Custom |
| Google TTS | Languages, SSML | 400+ |

## Use Cases

| Use Case | Modalities |
|----------|------------|
| Document analysis | Vision → Text |
| Video narration | Video → Speech → TTS |
| Voice assistant | Speech → LLM → TTS |
| Content generation | Text → Images/Video |
| Accessibility | Vision → TTS, Speech → Text |

## Related Skills

| Skill | Relationship |
|-------|-------------|
| faion-llm-integration | Provides vision APIs |
| faion-ai-agents | Multimodal agents |

---

*Multimodal AI v1.0 | 12 methodologies*
