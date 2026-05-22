---
name: "groq-inference"
description: "Fast LLM inference with Groq API - chat, vision, audio STT/TTS, tool use. Use when: groq, fast inference, low latency, whisper, PlayAI TTS, Llama, vision API, tool calling, voice agents, real-time AI."
---

# GROQ Inference Skill

Ultra-fast LLM inference for real-time applications. GROQ delivers 10-100x faster inference than standard providers.

## Quick Reference: Model Selection

| Use Case | Model ID | Context | Notes |
|----------|----------|---------|-------|
| **General Chat** | `llama-3.3-70b-versatile` | 128K | Best all-around |
| **Fast Chat** | `llama-3.1-8b-instant` | 128K | Simple tasks, fastest |
| **Vision/OCR** | `meta-llama/llama-4-scout-17b-16e-instruct` | 128K | Up to 5 images |
| **STT** | `whisper-large-v3` | 448 | GROQ-hosted (NOT OpenAI API) |
| **TTS** | `playai-tts` | - | Fritz-PlayAI voice |
| **Reasoning** | `meta-llama/llama-4-maverick-17b-128e-instruct` | 128K | Thinking models |
| **Tool Use** | `compound-beta` | - | Built-in web search, code exec |

## Core Patterns

### 1. Chat Completion (Basic + Streaming)

```python
import os
from groq import Groq, AsyncGroq

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def chat(prompt: str, system: str = "You are helpful.") -> str:
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_completion_tokens=1024,
    )
    return response.choices[0].message.content

# Streaming
def stream_chat(prompt: str):
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
```

### 2. Vision / Multimodal

```python
import base64

def analyze_image(image_path: str, prompt: str) -> str:
    with open(image_path, "rb") as f:
        image_b64 = base64.standard_b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
            ]
        }],
    )
    return response.choices[0].message.content

# URL-based: just pass {"url": "https://..."} instead of base64
```

### 3. Audio: Speech-to-Text (GROQ-Hosted Whisper)

> **Note:** Whisper on GROQ runs on **GROQ hardware** - NOT calling OpenAI's API.
> Whisper is an open-source model that GROQ hosts for fast inference.

```python
def transcribe(audio_path: str, language: str = "en") -> str:
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            model="whisper-large-v3",  # GROQ-hosted, not OpenAI API
            language=language,
            response_format="verbose_json",  # Includes timestamps
        )
    return result.text

def translate_to_english(audio_path: str) -> str:
    with open(audio_path, "rb") as f:
        result = client.audio.translations.create(file=f, model="whisper-large-v3")
    return result.text
```

**Alternative STT Providers** (if you prefer non-Whisper options):
- **Deepgram** - Real-time streaming, lowest latency (`pip install deepgram-sdk`)
- **AssemblyAI** - High accuracy, speaker diarization (`pip install assemblyai`)
- See `voice-ai-skill` for Deepgram/AssemblyAI integration patterns

### 4. Audio: Text-to-Speech (PlayAI)

```python
def text_to_speech(text: str, output_path: str = "output.wav"):
    response = client.audio.speech.create(
        model="playai-tts",
        voice="Fritz-PlayAI",  # Also: Arista-PlayAI
        input=text,
        response_format="wav",
    )
    response.write_to_file(output_path)

# Streaming TTS
def stream_tts(text: str):
    with client.audio.speech.with_streaming_response.create(
        model="playai-tts", voice="Fritz-PlayAI", input=text, response_format="wav"
    ) as response:
        for chunk in response.iter_bytes(1024):
            yield chunk
```

**Alternative TTS Providers** (beyond GROQ's PlayAI):
- **Cartesia** - Ultra-low latency, emotional control (`pip install cartesia`)
- **ElevenLabs** - Most natural voices, voice cloning (`pip install elevenlabs`)
- **Deepgram** - Fast, cost-effective (`pip install deepgram-sdk`)
- See `voice-ai-skill` for Cartesia/ElevenLabs/Deepgram TTS integration patterns

### 5. Tool Use / Function Calling

```python
import json

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }
}]

def chat_with_tools(prompt: str):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", messages=messages, tools=tools, tool_choice="auto"
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        for tc in msg.tool_calls:
            result = execute_function(tc.function.name, json.loads(tc.function.arguments))
            messages.extend([msg, {"role": "tool", "tool_call_id": tc.id, "content": json.dumps(result)}])
        return client.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, tools=tools).choices[0].message.content
    return msg.content
```

### 6. Compound Beta (Built-in Web Search + Code Exec)

```python
def compound_query(prompt: str):
    """Built-in tools: web_search, code_execution."""
    response = client.chat.completions.create(
        model="compound-beta",
        messages=[{"role": "user", "content": prompt}],
    )
    msg = response.choices[0].message
    # Access msg.executed_tools for tool results
    return msg.content
```

### 7. Reasoning Models

```python
def reasoning_query(prompt: str, format: str = "parsed"):
    """format: 'parsed' (structured), 'raw' (visible), 'hidden' (no thinking)"""
    response = client.chat.completions.create(
        model="meta-llama/llama-4-maverick-17b-128e-instruct",
        messages=[{"role": "user", "content": prompt}],
        reasoning_format=format,
    )
    msg = response.choices[0].message
    if format == "parsed" and hasattr(msg, 'reasoning'):
        return {"thinking": msg.reasoning, "answer": msg.content}
    return msg.content
```

### 8. Async Patterns

```python
async_client = AsyncGroq(api_key=os.environ.get("GROQ_API_KEY"))

async def async_chat(prompt: str) -> str:
    response = await async_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

async def parallel_queries(prompts: list[str]) -> list[str]:
    import asyncio
    return await asyncio.gather(*[async_chat(p) for p in prompts])
```

## Rate Limits

| Tier | Requests/min | Tokens/min | Tokens/day |
|------|--------------|------------|------------|
| Free | 30 | 15,000 | 500,000 |
| Paid | 100+ | 100,000+ | Unlimited |

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def reliable_chat(prompt: str) -> str:
    return chat(prompt)
```

## Integration Notes

- **Pairs with**: voice-ai-skill (Whisper STT + PlayAI TTS), langgraph-agents-skill
- **Complements**: trading-signals-skill (fast analysis), data-analysis-skill
- **Projects**: VozLux (voice agents), FieldVault-AI (document processing)
- **Constraint**: NO OPENAI - GROQ is the fast inference layer

## Environment Variables

```bash
GROQ_API_KEY=gsk_...  # Required - get from console.groq.com

# Optional multi-provider
ANTHROPIC_API_KEY=    # Claude for complex reasoning
GOOGLE_API_KEY=       # Gemini fallback
```

## Reference Files

- `reference/models-catalog.md` - Complete model catalog with specs
- `reference/audio-speech.md` - Whisper STT and PlayAI TTS deep dive
- `reference/vision-multimodal.md` - Multimodal and image processing
- `reference/tool-use-patterns.md` - Function calling and Compound Beta
- `reference/reasoning-models.md` - Thinking models and reasoning_format
- `reference/cost-optimization.md` - Batch API, caching, provider routing
