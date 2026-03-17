---
name: gemini-api-full
description: |
  Comprehensive reference for Google's Gemini API. Use when building applications with:
  (1) Gemini models (Gemini 3 Pro, 2.5 Flash/Pro/Flash-Lite) for text and multimodal generation,
  (2) Image generation (Imagen, Nano Banana), video (Veo 3.1), music (Lyria),
  (3) Function calling, structured outputs, and agentic workflows,
  (4) Built-in tools: Google Search, Maps, Code Execution, URL Context, Computer Use, File Search,
  (5) Live API for real-time voice/video streaming,
  (6) Long context (1M+ tokens), embeddings, document/audio/video understanding,
  (7) Batch API, context caching, safety settings.
  Triggers: "gemini api", "google ai", "genai sdk", "gemini model", "veo", "imagen", "nano banana", "lyria", "live api", "vertex ai"
---

# Gemini API Skill

Build AI applications with Google's Gemini models and tools.

## Quick Start

### Installation

```bash
# Python
pip install google-genai

# JavaScript/Node.js
npm install @google/genai

# Go
go get google.golang.org/genai
```

### Environment Setup

```bash
export GEMINI_API_KEY="your-api-key"
```

### Basic Usage

**Python:**
```python
from google import genai

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Your prompt here"
)
print(response.text)
```

**JavaScript:**
```javascript
import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});
const response = await ai.models.generateContent({
    model: "gemini-2.5-flash",
    contents: "Your prompt here"
});
console.log(response.text);
```

**REST:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents": [{"parts": [{"text": "Your prompt here"}]}]}'
```

## Model Selection

| Model | Best For | Context Window |
|-------|----------|----------------|
| **Gemini 3 Pro** | Most intelligent tasks, multimodal reasoning, agentic | See models-overview |
| **Gemini 2.5 Pro** | Complex reasoning, coding, extended thinking | 1M tokens |
| **Gemini 2.5 Flash** | Balanced performance, general tasks | 1M tokens |
| **Gemini 2.5 Flash-Lite** | High-volume, cost-sensitive, fastest | See models-overview |
| **Imagen** | High-fidelity image generation | N/A |
| **Veo 3.1** | Video generation (8s, 720p/1080p with audio) | N/A |
| **Nano Banana** | Native image gen with Gemini 2.5 Flash | N/A |
| **Nano Banana Pro** | Native image gen with Gemini 3 Pro | N/A |

## Reference Documentation Index

### Getting Started
| Topic | File | Description |
|-------|------|-------------|
| Setup & Libraries | [getting-started.md](references/getting-started.md) | API keys, SDK installation, OpenAI compatibility |

### Models & Pricing
| Topic | File | Description |
|-------|------|-------------|
| Model Overview | [models-overview.md](references/models-overview.md) | All models, capabilities, context windows |
| Pricing | [api-pricing.md](references/api-pricing.md) | Token costs, tool pricing |
| Rate Limits | [rate-limits.md](references/rate-limits.md) | RPM/TPM limits, quotas |
| Gemini 3 Guide | [gemini-3.md](references/gemini-3.md) | Gemini 3 specific features and best practices |
| Imagen | [imagen.md](references/imagen.md) | Image generation with Imagen model |
| Embeddings | [embeddings.md](references/embeddings.md) | Text embeddings for search/RAG |
| Veo | [veo.md](references/veo.md) | Video generation with Veo 3.1 (69K) |
| Lyria | [lyria.md](references/lyria.md) | Music generation with Lyria RealTime |
| Robotics | [robotics.md](references/robotics.md) | Gemini Robotics-ER 1.5 (42K) |

### Core Capabilities
| Topic | File | Description |
|-------|------|-------------|
| Text Generation | [text-generation.md](references/text-generation.md) | Text generation, system instructions (38K) |
| Image Gen (Nano Banana) | [image-generation-gemini.md](references/image-generation-gemini.md) | Native image generation with Gemini (LARGE: 174K) |
| Image Understanding | [image-understanding.md](references/image-understanding.md) | Vision, image analysis |
| Video Understanding | [video-understanding.md](references/video-understanding.md) | Video analysis, timestamps |
| Document Understanding | [document-understanding.md](references/document-understanding.md) | PDF and document processing |
| Speech Generation | [speech-generation.md](references/speech-generation.md) | Text-to-speech (TTS) |
| Audio Understanding | [audio-understanding.md](references/audio-understanding.md) | Audio analysis, transcription |

### Advanced Features
| Topic | File | Description |
|-------|------|-------------|
| Thinking Mode | [thinking.md](references/thinking.md) | Extended reasoning capabilities |
| Thought Signatures | [thought-signatures.md](references/thought-signatures.md) | **EDGE CASE ONLY**: Manual signature handling when NOT using official SDKs |
| Structured Outputs | [structured-outputs.md](references/structured-outputs.md) | JSON schema responses |
| Function Calling | [function-calling.md](references/function-calling.md) | Custom tool integration (54K) |
| Long Context | [long-context.md](references/long-context.md) | 1M+ token handling, context caching |

### Tools
| Topic | File | Description |
|-------|------|-------------|
| Tools Overview | [tools-overview.md](references/tools-overview.md) | Built-in tools summary, agent frameworks |
| Google Search | [google-search.md](references/google-search.md) | Web search grounding |
| Google Maps | [google-maps.md](references/google-maps.md) | Location-aware grounding |
| Code Execution | [code-execution.md](references/code-execution.md) | Python code execution tool |
| URL Context | [url-context.md](references/url-context.md) | URL content extraction |
| Computer Use | [computer-use.md](references/computer-use.md) | Browser automation (preview) (44K) |
| File Search | [file-search.md](references/file-search.md) | RAG with document indexing |

### Live API (Real-time Streaming)
| Topic | File | Description |
|-------|------|-------------|
| Getting Started | [live-api-getting-started.md](references/live-api-getting-started.md) | Low-latency voice/video interactions |
| Capabilities Guide | [live-api-capabilities.md](references/live-api-capabilities.md) | Full capabilities and configurations (32K) |
| Tool Use | [live-api-tools.md](references/live-api-tools.md) | Function calling & Search in Live API |
| Session Management | [live-api-sessions.md](references/live-api-sessions.md) | Session handling, time limits |
| Ephemeral Tokens | [ephemeral-tokens.md](references/ephemeral-tokens.md) | Short-lived auth for client-side WebSockets |

### Guides
| Topic | File | Description |
|-------|------|-------------|
| Batch API | [batch-api.md](references/batch-api.md) | Async processing at 50% cost (47K) |
| Files API | [files-api.md](references/files-api.md) | Upload and manage media files (49K) |
| Context Caching | [context-caching.md](references/context-caching.md) | Implicit & explicit caching for cost savings |
| Media Resolution | [media-resolution.md](references/media-resolution.md) | Control token allocation for media |
| Tokens | [tokens.md](references/tokens.md) | Understand and count tokens |
| Prompt Design | [prompt-design.md](references/prompt-design.md) | Prompt strategies and best practices (47K) |
| Logs & Datasets | [logs-datasets.md](references/logs-datasets.md) | Enable logging, view in AI Studio |
| Data Logging & Sharing | [data-logging-sharing.md](references/data-logging-sharing.md) | Storage and management of API logs |
| Safety Settings | [safety-settings.md](references/safety-settings.md) | Adjust safety filters |
| Safety Guidance | [safety-guidance.md](references/safety-guidance.md) | Best practices for safe AI use |

### Troubleshooting & Migration
| Topic | File | Description |
|-------|------|-------------|
| Troubleshooting | [troubleshooting.md](references/troubleshooting.md) | Diagnose and resolve common API issues (25K) |
| Vertex AI Comparison | [vertex-ai-comparison.md](references/vertex-ai-comparison.md) | **READ ONLY IF USER MENTIONS "VERTEX AI"**: Gemini Developer API vs Vertex AI differences |

### API Reference (Technical Endpoints)
> **Note:** These are technical endpoint specifications with schemas and parameter details. For usage guides and code examples, see the guide files above.

| Topic | File | Description |
|-------|------|-------------|
| Overview | [api-reference-overview.md](references/api-reference-overview.md) | REST/streaming/realtime API overview (33K) |
| Models Endpoint | [api-models-reference.md](references/api-models-reference.md) | models.get, models.list, models.predict |
| Generate Content | [api-generate-content.md](references/api-generate-content.md) | generateContent + all response types (LARGE: 166K) |
| Live API WebSockets | [api-live-websockets.md](references/api-live-websockets.md) | WebSockets API for Live API (48K) |
| Live Music WebSockets | [api-live-music-websockets.md](references/api-live-music-websockets.md) | WebSockets API for Lyria RealTime |
| Files Endpoint | [api-files-reference.md](references/api-files-reference.md) | Upload/manage media files (40K) |
| Batch Endpoint | [api-batch-reference.md](references/api-batch-reference.md) | Batch processing endpoints (40K) |
| Caching Endpoint | [api-caching-reference.md](references/api-caching-reference.md) | Context caching endpoints (LARGE: 89K) |
| Embeddings Endpoint | [api-embeddings-reference.md](references/api-embeddings-reference.md) | Embeddings generation endpoints (30K) |
| File Search Stores | [api-file-search-reference.md](references/api-file-search-reference.md) | File Search + Documents endpoints (35K) |

## Large Files - Search Patterns

For large reference files (>30K), use grep to find specific sections:

**image-generation-gemini.md (174K):**
```bash
grep -n "## " references/image-generation-gemini.md  # List sections
grep -n "edit" references/image-generation-gemini.md  # Find editing info
grep -n "style" references/image-generation-gemini.md  # Find style transfer
```

**api-generate-content.md (166K):**
```bash
grep -n "## " references/api-generate-content.md  # List sections
grep -n "GenerationConfig" references/api-generate-content.md  # Config options
grep -n "SafetySetting" references/api-generate-content.md  # Safety types
```

**api-caching-reference.md (89K):**
```bash
grep -n "## " references/api-caching-reference.md  # List sections
grep -n "CachedContent" references/api-caching-reference.md  # Cache types
```

**veo.md (69K):**
```bash
grep -n "## " references/veo.md  # List sections
grep -n "audio" references/veo.md  # Find audio generation info
```

**models-overview.md (67K):**
```bash
grep -n "gemini-3" references/models-overview.md
grep -n "context" references/models-overview.md
```

**function-calling.md (54K):**
```bash
grep -n "## " references/function-calling.md
grep -n "parallel" references/function-calling.md  # Parallel function calls
```

## Common Patterns

### Multimodal Input (Image + Text)
```python
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[
        types.Part.from_image(image_path),
        types.Part.from_text("Describe this image")
    ]
)
```

### Function Calling
```python
tools = [
    types.Tool(function_declarations=[{
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"]
        }
    }])
]

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What's the weather in Paris?",
    config=types.GenerateContentConfig(tools=tools)
)
```

### Google Search Grounding
```python
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="What are the latest AI developments?",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())]
    )
)
```

### Thinking Mode
```python
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents="Solve this complex problem...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget_tokens=10000)
    )
)
```

### Streaming
```python
for chunk in client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents="Write a story"
):
    print(chunk.text, end="")
```

## Key Concepts

### Tool Execution Flow

**Built-in tools** (Google Search, Code Execution): Executed by Google
1. Send prompt with tool config → Model executes tool → Response with grounded results

**Custom tools** (Function Calling): You execute
1. Send prompt with function declarations → Model returns function call JSON
2. You execute function, send result back → Model generates final response

### Thought Signatures (Important)
- **If using official SDKs with chat feature**: Thought signatures are handled automatically. No action needed.
- **If manually managing conversation history**: Read [thought-signatures.md](references/thought-signatures.md) for Gemini 3 Pro function calling requirements.

## API Endpoints

| Endpoint | Purpose |
|----------|---------|
| `/v1beta/models/{model}:generateContent` | Standard generation |
| `/v1beta/models/{model}:streamGenerateContent` | Streaming |
| `/v1beta/models/{model}:embedContent` | Embeddings |
| `/v1beta/models/{model}:countTokens` | Token counting |

Base URL: `https://generativelanguage.googleapis.com`
