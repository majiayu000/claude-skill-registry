---
name: gemini-api
description: Google Gemini API integration for building AI-powered applications. Use when working with Google's Gemini API, Python SDK (google-genai), TypeScript SDK (@google/genai), multimodal inputs (image, video, audio, PDF), thinking/reasoning features, streaming responses, structured outputs with JSON schemas, multi-turn chat, system instructions, image generation (Nano Banana), video generation (Veo), music generation (Lyria), embeddings, document/PDF processing, or any Gemini API integration task. Triggers on mentions of Gemini, Gemini 3, Gemini 2.5, Google AI, Nano Banana, Veo, Lyria, google-genai, or @google/genai SDK usage.
---

# Gemini API

Generate text from text, images, video, and audio using Google's Gemini API.

## Models

| Model | Code | I/O | Context | Thinking |
|-------|------|-----|---------|----------|
| **Gemini 3 Pro** | `gemini-3-pro-preview` | Text/Image/Video/Audio/PDF -> Text | 1M/64K | Yes |
| **Gemini 3 Flash** | `gemini-3-flash-preview` | Text/Image/Video/Audio/PDF -> Text | 1M/64K | Yes |
| **Gemini 2.5 Pro** | `gemini-2.5-pro` | Text/Image/Video/Audio/PDF -> Text | 1M/65K | Yes |
| **Gemini 2.5 Flash** | `gemini-2.5-flash` | Text/Image/Video/Audio -> Text | 1M/65K | Yes |
| **Nano Banana** | `gemini-2.5-flash-image` | Text/Image -> Image | - | No |
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | Text/Image -> Image (up to 4K) | 65K/32K | Yes |
| **Veo 3.1** | `veo-3.1-generate-preview` | Text/Image/Video -> Video+Audio | - | - |
| **Veo 3** | `veo-3-generate-preview` | Text/Image -> Video+Audio | - | - |
| **Veo 2** | `veo-2.0-generate-001` | Text/Image -> Video (silent) | - | - |
| **Lyria RealTime** | `lyria-realtime-exp` | Text -> Music (streaming) | - | - |
| **Embeddings** | `gemini-embedding-001` | Text -> Embeddings | 2K | No |

**Free Tier**: Flash models only (no free tier for `gemini-3-pro-preview` in API). **Default Temperature**: 1.0 (do not change for Gemini 3).

**Pricing (per 1M tokens)**:
- Gemini 3 Pro: $2/$12 (<200k), $4/$18 (>200k)
- Gemini 3 Flash: $0.50/$3
- Nano Banana Pro: $2 (text) / $0.134 (image)

---

## Basic Text Generation

### Python
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="How does AI work?"
)
print(response.text)
```

### JavaScript
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "How does AI work?",
});
console.log(response.text);
```

### REST
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents": [{"parts": [{"text": "How does AI work?"}]}]}'
```

---

## System Instructions

```python
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    config=types.GenerateContentConfig(
        system_instruction="You are a helpful assistant."
    ),
    contents="Hello"
)
```

```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Hello",
  config: { systemInstruction: "You are a helpful assistant." },
});
```

---

## Streaming

```python
for chunk in client.models.generate_content_stream(
    model="gemini-3-flash-preview",
    contents="Tell me a story"
):
    print(chunk.text, end="")
```

```javascript
const response = await ai.models.generateContentStream({
  model: "gemini-3-flash-preview",
  contents: "Tell me a story",
});
for await (const chunk of response) {
  console.log(chunk.text);
}
```

---

## Multi-turn Chat

```python
chat = client.chats.create(model="gemini-3-flash-preview")
response = chat.send_message("I have 2 dogs.")
print(response.text)
response = chat.send_message("How many paws total?")
print(response.text)
```

```javascript
const chat = ai.chats.create({ model: "gemini-3-flash-preview" });
const response = await chat.sendMessage({ message: "I have 2 dogs." });
console.log(response.text);
```

---

## Multimodal (Image)

```python
from PIL import Image

image = Image.open("/path/to/image.png")
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[image, "Describe this image"]
)
```

```javascript
const image = await ai.files.upload({ file: "/path/to/image.png" });
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: [
    createUserContent([
      "Describe this image",
      createPartFromUri(image.uri, image.mimeType),
    ]),
  ],
});
```

---

## Document Processing (PDF)

Process PDFs with native vision understanding (up to 1000 pages).

```python
from google.genai import types
import pathlib

filepath = pathlib.Path('document.pdf')
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[
        types.Part.from_bytes(data=filepath.read_bytes(), mime_type='application/pdf'),
        "Summarize this document"
    ]
)
```

```javascript
import * as fs from 'fs';

const response = await ai.models.generateContent({
    model: "gemini-3-flash-preview",
    contents: [
        { text: "Summarize this document" },
        {
            inlineData: {
                mimeType: 'application/pdf',
                data: Buffer.from(fs.readFileSync("document.pdf")).toString("base64")
            }
        }
    ]
});
```

**For large PDFs**, use Files API (stored 48 hours):

```python
uploaded_file = client.files.upload(file=pathlib.Path('large.pdf'))
response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[uploaded_file, "Summarize this document"]
)
```

See [references/documents.md](references/documents.md) for Files API, multiple PDFs, and best practices.

---

## Image Generation (Nano Banana)

Generate and edit images conversationally.

```python
response = client.models.generate_content(
    model="gemini-2.5-flash-image",
    contents="Create a picture of a sunset over mountains",
)

for part in response.parts:
    if part.inline_data is not None:
        part.as_image().save("generated.png")
```

```javascript
const response = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: "Create a picture of a sunset over mountains",
});

for (const part of response.candidates[0].content.parts) {
  if (part.inlineData) {
    const buffer = Buffer.from(part.inlineData.data, "base64");
    fs.writeFileSync("generated.png", buffer);
  }
}
```

**Nano Banana Pro** (`gemini-3-pro-image-preview`): 4K output, Google Search grounding, up to 14 reference images, conversational editing with thought signatures.

See [references/image-generation.md](references/image-generation.md) for editing, multi-turn, and advanced features.
See [references/gemini-3.md](references/gemini-3.md#nano-banana-pro-image-generation) for Gemini 3 image capabilities.

---

## Video Generation (Veo)

Generate 8-second 720p, 1080p, or 4K videos with native audio using Veo.

```python
import time
from google import genai

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-preview",
    prompt="A cinematic shot of a majestic lion in the savannah at golden hour",
)

# Poll until complete (video generation is async)
while not operation.done:
    time.sleep(10)
    operation = client.operations.get(operation)

# Download the video
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("lion.mp4")
```

```javascript
let operation = await ai.models.generateVideos({
    model: "veo-3.1-generate-preview",
    prompt: "A cinematic shot of a majestic lion in the savannah at golden hour",
});

while (!operation.done) {
    await new Promise(resolve => setTimeout(resolve, 10000));
    operation = await ai.operations.getVideosOperation({ operation });
}

ai.files.download({
    file: operation.response.generatedVideos[0].video,
    downloadPath: "lion.mp4",
});
```

**Veo 3.1 features**: Portrait (9:16), video extension (up to 148s), 4K resolution, native audio with dialogue/SFX.

See [references/veo.md](references/veo.md) for image-to-video, reference images, video extension, and prompting guide.

---

## Music Generation (Lyria RealTime)

Generate continuous instrumental music in real-time with dynamic steering.

```python
import asyncio
from google import genai
from google.genai import types

client = genai.Client()

async def main():
    async with client.aio.live.music.connect(model='models/lyria-realtime-exp') as session:
        # Set prompts and config
        await session.set_weighted_prompts(
            prompts=[types.WeightedPrompt(text='minimal techno', weight=1.0)]
        )
        await session.set_music_generation_config(
            config=types.LiveMusicGenerationConfig(bpm=90, temperature=1.0)
        )

        # Start streaming
        await session.play()

        # Receive audio chunks
        async for message in session.receive():
            if message.server_content and message.server_content.audio_chunks:
                audio_data = message.server_content.audio_chunks[0].data
                # Process audio...

asyncio.run(main())
```

```javascript
const session = await ai.live.music.connect({
    model: "models/lyria-realtime-exp",
    callbacks: {
        onmessage: (message) => {
            if (message.serverContent?.audioChunks) {
                for (const chunk of message.serverContent.audioChunks) {
                    const audioBuffer = Buffer.from(chunk.data, "base64");
                    // Process audio...
                }
            }
        },
    },
});

await session.setWeightedPrompts({
    weightedPrompts: [{ text: "minimal techno", weight: 1.0 }],
});

await session.setMusicGenerationConfig({
    musicGenerationConfig: { bpm: 90, temperature: 1.0 },
});

await session.play();
```

**Output**: 48kHz stereo 16-bit PCM. **Instrumental only**. Configurable BPM, scale, density, brightness.

See [references/lyria.md](references/lyria.md) for steering music, configuration, and prompting guide.

---

## Embeddings

Generate text embeddings for semantic similarity, search, and classification.

```python
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents="What is the meaning of life?"
)
print(result.embeddings)
```

```javascript
const response = await ai.models.embedContent({
    model: 'gemini-embedding-001',
    contents: 'What is the meaning of life?',
});
console.log(response.embeddings);
```

**Task types**: `SEMANTIC_SIMILARITY`, `CLASSIFICATION`, `CLUSTERING`, `RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`

**Output dimensions**: 768, 1536, 3072 (default)

See [references/embeddings.md](references/embeddings.md) for batch processing, task types, and normalization.

---

## Thinking (Gemini 3)

Control reasoning depth with `thinking_level`: `minimal` (Flash only), `low`, `medium` (Flash only), `high` (default).

```python
from google.genai import types

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Solve this math problem...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high")
    ),
)
```

```javascript
import { ThinkingLevel } from "@google/genai";

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Solve this math problem...",
  config: { thinkingConfig: { thinkingLevel: ThinkingLevel.HIGH } },
});
```

**Note**: Cannot mix `thinking_level` with legacy `thinking_budget` (returns 400 error).

For Gemini 2.5, use `thinking_budget` (0-32768) instead. See [references/thinking.md](references/thinking.md).

For complete Gemini 3 features (thought signatures, media resolution, etc.), see [references/gemini-3.md](references/gemini-3.md).

---

## Structured Outputs

Generate JSON responses adhering to a schema.

```python
from pydantic import BaseModel
from typing import List

class Recipe(BaseModel):
    name: str
    ingredients: List[str]

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="Extract: chocolate chip cookies need flour, sugar, chips",
    config={
        "response_mime_type": "application/json",
        "response_json_schema": Recipe.model_json_schema(),
    },
)
recipe = Recipe.model_validate_json(response.text)
```

```javascript
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const recipeSchema = z.object({
  name: z.string(),
  ingredients: z.array(z.string()),
});

const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "Extract: chocolate chip cookies need flour, sugar, chips",
  config: {
    responseMimeType: "application/json",
    responseJsonSchema: zodToJsonSchema(recipeSchema),
  },
});
```

See [references/structured-outputs.md](references/structured-outputs.md) for advanced patterns.

---

## Built-in Tools (Gemini 3)

**Available**: Google Search, File Search, Code Execution, URL Context, Function Calling

**Not supported**: Google Maps grounding, Computer Use (use Gemini 2.5 for these)

```python
response = client.models.generate_content(
    model="gemini-3-pro-preview",
    contents="What's the latest news on AI?",
    config={"tools": [{"google_search": {}}]},
)
```

```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-pro-preview",
  contents: "What's the latest news on AI?",
  config: { tools: [{ googleSearch: {} }] },
});
```

**Structured outputs + tools**: Gemini 3 supports combining JSON schemas with built-in tools (Google Search, URL Context, Code Execution). See [references/gemini-3.md](references/gemini-3.md#structured-outputs-with-built-in-tools).

See [references/tools.md](references/tools.md) for all tool patterns.

---

## Function Calling

Connect models to external tools and APIs. The model determines when to call functions and provides parameters.

```python
from google.genai import types

# Define function
get_weather = {
    "name": "get_weather",
    "description": "Get weather for a location",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City name"},
        },
        "required": ["location"],
    },
}

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="What's the weather in Tokyo?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(function_declarations=[get_weather])]
    ),
)

# Check for function call
if response.function_calls:
    fc = response.function_calls[0]
    print(f"Call {fc.name} with {fc.args}")
```

```javascript
const response = await ai.models.generateContent({
  model: "gemini-3-flash-preview",
  contents: "What's the weather in Tokyo?",
  config: {
    tools: [{ functionDeclarations: [getWeather] }],
  },
});

if (response.functionCalls) {
  const { name, args } = response.functionCalls[0];
  // Execute function and send result back
}
```

**Automatic function calling (Python)**: Pass functions directly as tools for automatic execution.

See [references/function-calling.md](references/function-calling.md) for execution modes, compositional calling, multimodal responses, MCP integration, and best practices.

---

## Quick Reference

| Feature | Python | JavaScript |
|---------|--------|------------|
| Generate | `generate_content()` | `generateContent()` |
| Stream | `generate_content_stream()` | `generateContentStream()` |
| Chat | `chats.create()` | `chats.create()` |
| Structured | `response_json_schema=` | `responseJsonSchema:` |
| Image Gen | `gemini-2.5-flash-image` | `gemini-2.5-flash-image` |
| Video Gen | `generate_videos()` | `generateVideos()` |
| Music Gen | `live.music.connect()` | `live.music.connect()` |
| Function Call | `function_declarations` | `functionDeclarations` |
| Embeddings | `embed_content()` | `embedContent()` |
| Files API | `files.upload()` | `files.upload()` |

---

## Gemini 3 Specific Features

For advanced Gemini 3 features, see [references/gemini-3.md](references/gemini-3.md):

- **Thinking levels**: Control reasoning depth (`minimal`, `low`, `medium`, `high`)
- **Media resolution**: Fine-grained multimodal processing (`media_resolution_low` to `ultra_high`)
- **Thought signatures**: Required for function calling and image editing context
- **Structured outputs + tools**: Combine JSON schemas with Google Search, URL Context
- **Multimodal function responses**: Return images in tool responses

---

## Resources

- [Gemini 3 Guide](https://ai.google.dev/gemini-api/docs/gemini-3)
- [Models Overview](https://ai.google.dev/gemini-api/docs/models)
- [Thinking Guide](https://ai.google.dev/gemini-api/docs/thinking)
- [Thought Signatures](https://ai.google.dev/gemini-api/docs/thought-signatures)
- [Structured Outputs](https://ai.google.dev/gemini-api/docs/structured-output)
- [Image Generation](https://ai.google.dev/gemini-api/docs/image-generation)
- [Video Generation (Veo)](https://ai.google.dev/gemini-api/docs/video)
- [Music Generation (Lyria)](https://ai.google.dev/gemini-api/docs/music-generation)
- [Function Calling](https://ai.google.dev/gemini-api/docs/function-calling)
- [Document Processing](https://ai.google.dev/gemini-api/docs/document-processing)
- [Embeddings](https://ai.google.dev/gemini-api/docs/embeddings)
- [Google AI Studio](https://aistudio.google.com)
- [Gemini 3 Pro in AI Studio](https://aistudio.google.com?model=gemini-3-pro-preview)
- [Gemini 3 Flash in AI Studio](https://aistudio.google.com?model=gemini-3-flash-preview)
- [Nano Banana Pro in AI Studio](https://aistudio.google.com?model=gemini-3-pro-image-preview)
- [Veo Studio](https://aistudio.google.com/apps/bundled/veo_studio)
