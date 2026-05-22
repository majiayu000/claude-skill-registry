---
name: faion-openai-api-skill
user-invocable: false
description: ""
---

# OpenAI API Mastery

**Complete Guide to OpenAI Platform (2025-2026)**

---

## Quick Reference

| API | Endpoint | Best Model | Use Case |
|-----|----------|------------|----------|
| **Chat Completions** | `/v1/chat/completions` | gpt-4o | Text generation, conversation |
| **Responses** | `/v1/responses` | gpt-4o | Simplified stateful API |
| **Vision** | `/v1/chat/completions` | gpt-4o | Image understanding |
| **Function Calling** | `/v1/chat/completions` | gpt-4o | Tool use, structured output |
| **DALL-E** | `/v1/images/generations` | dall-e-3 | Image generation |
| **Whisper** | `/v1/audio/transcriptions` | whisper-1 | Speech-to-text |
| **TTS** | `/v1/audio/speech` | tts-1-hd | Text-to-speech |
| **Embeddings** | `/v1/embeddings` | text-embedding-3-large | Vector search, RAG |
| **Assistants** | `/v1/assistants` | gpt-4o | Stateful agents |
| **Batch** | `/v1/batches` | gpt-4o | 50% cost savings |
| **Realtime** | WebSocket | gpt-4o-realtime | Voice conversations |
| **Fine-tuning** | `/v1/fine_tuning/jobs` | gpt-4o-mini | Custom models |

---

## Authentication

### Setup

```bash
# Environment variable (recommended)
export OPENAI_API_KEY="sk-proj-..."

# Or load from file
source ~/.secrets/openai  # Loads OPENAI_API_KEY
```

### API Key Types

| Type | Prefix | Scope |
|------|--------|-------|
| **Project Key** | `sk-proj-` | Single project, recommended |
| **User Key** | `sk-` | All projects (legacy) |
| **Service Account** | `sk-svcacct-` | Automated systems |

### Headers

```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Organization: org-xxxxx" \  # Optional
  -H "OpenAI-Project: proj-xxxxx"         # Optional
```

---

## Chat Completions API

### Basic Request

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain SDD methodology in 3 sentences."}
    ]
)

print(response.choices[0].message.content)
```

### Models

| Model | Context | Input $/M | Output $/M | Best For |
|-------|---------|-----------|------------|----------|
| **gpt-4o** | 128K | $2.50 | $10.00 | General purpose, best quality |
| **gpt-4o-mini** | 128K | $0.15 | $0.60 | Cost-effective, fast |
| **gpt-4o-audio-preview** | 128K | $2.50 | $10.00 | Audio input/output |
| **gpt-4-turbo** | 128K | $10.00 | $30.00 | Legacy, replaced by 4o |
| **o1** | 128K | $15.00 | $60.00 | Complex reasoning |
| **o1-mini** | 128K | $1.10 | $4.40 | Reasoning, lower cost |
| **o3-mini** | 200K | $1.10 | $4.40 | Latest reasoning model |

### Parameters

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[...],

    # Generation
    temperature=0.7,        # 0-2, higher = more creative
    top_p=1.0,              # Nucleus sampling (alternative to temp)
    max_tokens=4096,        # Max response length
    n=1,                    # Number of completions

    # Control
    stop=["\n\n", "END"],   # Stop sequences
    presence_penalty=0.0,   # -2 to 2, penalize repeated topics
    frequency_penalty=0.0,  # -2 to 2, penalize repeated tokens

    # Format
    response_format={"type": "json_object"},  # Force JSON output
    seed=42,                # Deterministic outputs

    # Advanced
    logprobs=True,          # Return token probabilities
    top_logprobs=5,         # Number of logprobs per position
    user="user-123"         # Track abuse
)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a poem"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Message Roles

| Role | Purpose |
|------|---------|
| **system** | Set behavior, persona, instructions |
| **user** | User input |
| **assistant** | Model responses (for context) |
| **tool** | Tool/function results |

---

## Function Calling / Tool Use

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name, e.g., 'Kyiv'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"]
            }
        }
    }
]
```

### Request with Tools

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Kyiv?"}],
    tools=tools,
    tool_choice="auto"  # "auto" | "none" | "required" | {"type": "function", "function": {"name": "get_weather"}}
)

# Check if tool call was made
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your implementation
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

# Initial request
messages = [{"role": "user", "content": "What's the weather in Kyiv?"}]
response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools
)

message = response.choices[0].message
messages.append(message)  # Add assistant message

# Process tool calls
if message.tool_calls:
    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Get final response
    final_response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools
    )
    print(final_response.choices[0].message.content)
```

### Parallel Tool Calls

Model can call multiple tools simultaneously:

```python
# Response with multiple tool calls
{
    "tool_calls": [
        {"id": "call_1", "function": {"name": "get_weather", "arguments": "{\"location\": \"Kyiv\"}"}},
        {"id": "call_2", "function": {"name": "get_weather", "arguments": "{\"location\": \"London\"}"}}
    ]
}
```

### Structured Outputs (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    email: Optional[str]
    addresses: List[Address]

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30, john@example.com, lives at 123 Main St, Kyiv, Ukraine"}
    ],
    response_format=Person
)

person = response.choices[0].message.parsed
print(person.name)  # "John Doe"
print(person.addresses[0].city)  # "Kyiv"
```

---

## Vision API

### Image from URL

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What's in this image?"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://example.com/image.jpg",
                        "detail": "high"  # "low" | "high" | "auto"
                    }
                }
            ]
        }
    ]
)
```

### Image from Base64

```python
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

image_data = encode_image("screenshot.png")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Describe this screenshot"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{image_data}"
                    }
                }
            ]
        }
    ]
)
```

### Multiple Images

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two designs"},
                {"type": "image_url", "image_url": {"url": "https://example.com/design1.png"}},
                {"type": "image_url", "image_url": {"url": "https://example.com/design2.png"}}
            ]
        }
    ]
)
```

### Detail Levels

| Level | Tokens | Best For |
|-------|--------|----------|
| **low** | 85 | Quick overview, thumbnails |
| **high** | 85-1105+ | OCR, detailed analysis |
| **auto** | Varies | Model decides |

### Vision Limitations

- Max 20MB per image
- Supported: PNG, JPEG, GIF, WebP
- No video (extract frames)
- May struggle with: rotated text, small text, spatial reasoning

---

## DALL-E Image Generation

### Generate Images

```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A serene Japanese garden with a red bridge over a koi pond, photorealistic",
    size="1024x1024",      # "1024x1024" | "1792x1024" | "1024x1792"
    quality="hd",          # "standard" | "hd"
    style="vivid",         # "vivid" | "natural"
    n=1                    # DALL-E 3 only supports n=1
)

image_url = response.data[0].url
revised_prompt = response.data[0].revised_prompt  # DALL-E 3 rewrites prompts
```

### Response Formats

```python
# URL (default, expires in 1 hour)
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="url"
)

# Base64 (for immediate use)
response = client.images.generate(
    model="dall-e-3",
    prompt="...",
    response_format="b64_json"
)
image_b64 = response.data[0].b64_json
```

### Edit Images (DALL-E 2 only)

```python
response = client.images.edit(
    model="dall-e-2",
    image=open("original.png", "rb"),
    mask=open("mask.png", "rb"),  # Transparent areas will be regenerated
    prompt="Add a red sports car",
    size="1024x1024",
    n=1
)
```

### Create Variations (DALL-E 2 only)

```python
response = client.images.create_variation(
    model="dall-e-2",
    image=open("original.png", "rb"),
    size="1024x1024",
    n=3
)
```

### Pricing

| Model | Quality | Size | Price |
|-------|---------|------|-------|
| **DALL-E 3** | HD | 1024x1024 | $0.080 |
| **DALL-E 3** | HD | 1792x1024, 1024x1792 | $0.120 |
| **DALL-E 3** | Standard | 1024x1024 | $0.040 |
| **DALL-E 3** | Standard | 1792x1024, 1024x1792 | $0.080 |
| **DALL-E 2** | - | 1024x1024 | $0.020 |
| **DALL-E 2** | - | 512x512 | $0.018 |
| **DALL-E 2** | - | 256x256 | $0.016 |

### Prompt Tips

```
Style keywords: "photorealistic", "digital art", "oil painting", "3D render", "anime style"
Lighting: "soft lighting", "golden hour", "neon glow", "dramatic shadows"
Composition: "centered", "rule of thirds", "wide angle", "close-up", "aerial view"
Quality: "highly detailed", "8K resolution", "professional photography"
Mood: "serene", "dramatic", "playful", "mysterious", "minimalist"
```

---

## Whisper (Speech-to-Text)

### Transcription

```python
audio_file = open("speech.mp3", "rb")

transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="uk",           # ISO 639-1 code (optional)
    response_format="text",  # "json" | "text" | "srt" | "vtt" | "verbose_json"
    temperature=0.0,         # 0-1, lower = more deterministic
    prompt="SDD, Faion Network"  # Hints for proper nouns
)

print(transcript)  # Plain text for response_format="text"
```

### Verbose JSON (with timestamps)

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"]
)

for segment in transcript.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s] {segment.text}")
```

### Translation (to English)

```python
# Translates any language to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=open("ukrainian_speech.mp3", "rb"),
    response_format="text"
)
```

### Supported Formats

- mp3, mp4, mpeg, mpga, m4a, wav, webm
- Max file size: 25MB
- For longer files: split or use chunking

### Pricing

| Model | Price |
|-------|-------|
| whisper-1 | $0.006 / minute |

---

## TTS (Text-to-Speech)

### Generate Speech

```python
response = client.audio.speech.create(
    model="tts-1-hd",        # "tts-1" (fast) | "tts-1-hd" (quality)
    voice="nova",            # alloy | echo | fable | onyx | nova | shimmer
    input="Hello, welcome to Faion Network!",
    speed=1.0,               # 0.25 - 4.0
    response_format="mp3"    # mp3 | opus | aac | flac | wav | pcm
)

response.stream_to_file("output.mp3")
```

### Streaming

```python
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="Long text to speak..."
) as response:
    response.stream_to_file("output.mp3")
```

### Voice Characteristics

| Voice | Description |
|-------|-------------|
| **alloy** | Neutral, balanced |
| **echo** | Warm, authoritative |
| **fable** | British, expressive |
| **onyx** | Deep, rich |
| **nova** | Young, energetic |
| **shimmer** | Soft, gentle |

### Pricing

| Model | Price |
|-------|-------|
| tts-1 | $15.00 / 1M characters |
| tts-1-hd | $30.00 / 1M characters |

---

## Embeddings API

### Generate Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Faion Network provides AI tools for solopreneurs",
    encoding_format="float",  # "float" | "base64"
    dimensions=1536           # Optional, reduce for cost savings
)

embedding = response.data[0].embedding
print(f"Dimensions: {len(embedding)}")
```

### Batch Embeddings

```python
texts = [
    "What is SDD methodology?",
    "How to create AI agents?",
    "Faion Network pricing plans"
]

response = client.embeddings.create(
    model="text-embedding-3-large",
    input=texts
)

for i, item in enumerate(response.data):
    print(f"Text {i}: {len(item.embedding)} dimensions")
```

### Models

| Model | Dimensions | Max Tokens | Price $/M |
|-------|------------|------------|-----------|
| **text-embedding-3-large** | 3072 (or custom) | 8191 | $0.13 |
| **text-embedding-3-small** | 1536 (or custom) | 8191 | $0.02 |
| **text-embedding-ada-002** | 1536 | 8191 | $0.10 |

### Dimensionality Reduction

```python
# Reduce dimensions for cost/performance tradeoff
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="Your text",
    dimensions=256  # Reduced from 3072
)
```

### Cosine Similarity

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

query_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="How to use SDD?"
).data[0].embedding

doc_embedding = client.embeddings.create(
    model="text-embedding-3-small",
    input="SDD is a specification-driven methodology..."
).data[0].embedding

similarity = cosine_similarity(query_embedding, doc_embedding)
print(f"Similarity: {similarity:.4f}")
```

---

## Assistants API

### Create Assistant

```python
assistant = client.beta.assistants.create(
    model="gpt-4o",
    name="SDD Expert",
    instructions="You are an expert on Specification-Driven Development. Help users understand and apply SDD methodology.",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ],
    temperature=0.7,
    metadata={"version": "1.0"}
)
```

### Create Thread

```python
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "What are the key phases of SDD?"
        }
    ]
)
```

### Run Assistant

```python
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data:
        if message.role == "assistant":
            print(message.content[0].text.value)
```

### Streaming Run

```python
from openai import AssistantEventHandler

class EventHandler(AssistantEventHandler):
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\n[Using tool: {tool_call.type}]")

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler()
) as stream:
    stream.until_done()
```

### File Search (Knowledge Base)

```python
# Create vector store
vector_store = client.beta.vector_stores.create(name="SDD Documentation")

# Upload files
file = client.files.create(
    file=open("sdd-guide.pdf", "rb"),
    purpose="assistants"
)

client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id
)

# Attach to assistant
assistant = client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)
```

### Code Interpreter

```python
# Upload data file
file = client.files.create(
    file=open("data.csv", "rb"),
    purpose="assistants"
)

# Create thread with attachment
thread = client.beta.threads.create(
    messages=[
        {
            "role": "user",
            "content": "Analyze this data and create a chart",
            "attachments": [
                {"file_id": file.id, "tools": [{"type": "code_interpreter"}]}
            ]
        }
    ]
)
```

---

## Batch API

50% cost reduction for non-time-sensitive workloads with 24-hour completion window.

### Create Batch File

```python
import json

# Create JSONL file with requests
requests = [
    {
        "custom_id": "request-1",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "Hello!"}],
            "max_tokens": 100
        }
    },
    {
        "custom_id": "request-2",
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": "World!"}],
            "max_tokens": 100
        }
    }
]

with open("batch_requests.jsonl", "w") as f:
    for req in requests:
        f.write(json.dumps(req) + "\n")
```

### Submit Batch

```python
# Upload file
batch_file = client.files.create(
    file=open("batch_requests.jsonl", "rb"),
    purpose="batch"
)

# Create batch
batch = client.batches.create(
    input_file_id=batch_file.id,
    endpoint="/v1/chat/completions",
    completion_window="24h",
    metadata={"description": "Daily summaries"}
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.status}")
```

### Check Status

```python
batch = client.batches.retrieve(batch.id)
print(f"Status: {batch.status}")
print(f"Completed: {batch.request_counts.completed}/{batch.request_counts.total}")

if batch.status == "completed":
    # Download results
    result_file = client.files.content(batch.output_file_id)
    results = result_file.text

    for line in results.strip().split("\n"):
        result = json.loads(line)
        print(f"{result['custom_id']}: {result['response']['body']['choices'][0]['message']['content']}")
```

### Batch Pricing

| Model | Regular Price | Batch Price (50% off) |
|-------|--------------|----------------------|
| gpt-4o | $2.50/$10.00 | $1.25/$5.00 |
| gpt-4o-mini | $0.15/$0.60 | $0.075/$0.30 |

---

## Realtime API

WebSocket-based API for voice conversations.

### Connect

```python
import asyncio
import websockets
import json
import base64

async def realtime_conversation():
    url = "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
    headers = {
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
        "OpenAI-Beta": "realtime=v1"
    }

    async with websockets.connect(url, extra_headers=headers) as ws:
        # Configure session
        await ws.send(json.dumps({
            "type": "session.update",
            "session": {
                "modalities": ["text", "audio"],
                "voice": "alloy",
                "instructions": "You are a helpful assistant."
            }
        }))

        # Send user message
        await ws.send(json.dumps({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": "Hello!"}]
            }
        }))

        # Request response
        await ws.send(json.dumps({"type": "response.create"}))

        # Receive response
        async for message in ws:
            event = json.loads(message)
            if event["type"] == "response.audio_transcript.delta":
                print(event["delta"], end="", flush=True)
            elif event["type"] == "response.done":
                break

asyncio.run(realtime_conversation())
```

### Pricing

| Component | Price |
|-----------|-------|
| Audio input | $100.00 / 1M tokens |
| Audio output | $200.00 / 1M tokens |
| Text input | $5.00 / 1M tokens |
| Text output | $20.00 / 1M tokens |

---

## Fine-tuning

### Prepare Training Data

```jsonl
{"messages": [{"role": "system", "content": "You are an SDD expert."}, {"role": "user", "content": "What is SDD?"}, {"role": "assistant", "content": "SDD (Specification-Driven Development) is a methodology..."}]}
{"messages": [{"role": "user", "content": "How to write a spec?"}, {"role": "assistant", "content": "To write a spec, start with..."}]}
```

### Create Fine-tuning Job

```python
# Upload training file
training_file = client.files.create(
    file=open("training_data.jsonl", "rb"),
    purpose="fine-tune"
)

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto"
    },
    suffix="sdd-expert"
)
```

### Monitor Job

```python
# Check status
job = client.fine_tuning.jobs.retrieve(job.id)
print(f"Status: {job.status}")

# List events
events = client.fine_tuning.jobs.list_events(job.id, limit=10)
for event in events.data:
    print(f"{event.created_at}: {event.message}")
```

### Use Fine-tuned Model

```python
response = client.chat.completions.create(
    model="ft:gpt-4o-mini-2024-07-18:org-xxx:sdd-expert:abc123",
    messages=[{"role": "user", "content": "Explain SDD phases"}]
)
```

### Pricing

| Model | Training | Input | Output |
|-------|----------|-------|--------|
| gpt-4o-mini-2024-07-18 | $25.00/1M tokens | $3.00/1M | $12.00/1M |
| gpt-4o-2024-08-06 | $25.00/1M tokens | $3.75/1M | $15.00/1M |

---

## Error Handling

### Common Errors

| Error | HTTP Code | Cause | Solution |
|-------|-----------|-------|----------|
| `invalid_api_key` | 401 | Bad API key | Check OPENAI_API_KEY |
| `rate_limit_exceeded` | 429 | Too many requests | Implement exponential backoff |
| `insufficient_quota` | 429 | Usage limit reached | Add credits or wait for reset |
| `model_not_found` | 404 | Invalid model name | Check available models |
| `context_length_exceeded` | 400 | Too many tokens | Reduce input or use larger context model |
| `server_error` | 500 | OpenAI issue | Retry with backoff |

### Retry with Backoff

```python
import time
from openai import RateLimitError, APIError

def call_with_retry(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
        except APIError as e:
            if e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                print(f"Server error. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

# Usage
response = call_with_retry(
    lambda: client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
)
```

### Using tenacity Library

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from openai import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def make_request():
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}]
    )
```

---

## Rate Limiting

### Limits by Tier

| Tier | RPM | TPM | Daily |
|------|-----|-----|-------|
| **Free** | 3 | 200 | Limited |
| **Tier 1** | 500 | 30,000 | $100 |
| **Tier 2** | 5,000 | 450,000 | $500 |
| **Tier 3** | 5,000 | 800,000 | $1,000 |
| **Tier 4** | 10,000 | 2,000,000 | $5,000 |
| **Tier 5** | 10,000 | 10,000,000 | $50,000 |

### Check Rate Limit Headers

```python
response = client.chat.completions.with_raw_response.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi"}]
)

# Access headers
print(f"Requests remaining: {response.headers.get('x-ratelimit-remaining-requests')}")
print(f"Tokens remaining: {response.headers.get('x-ratelimit-remaining-tokens')}")
print(f"Reset in: {response.headers.get('x-ratelimit-reset-requests')}")
```

---

## Cost Tracking

### Token Counting

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# Count message tokens
messages = [
    {"role": "system", "content": "You are helpful."},
    {"role": "user", "content": "Hello world!"}
]

total = sum(count_tokens(m["content"]) for m in messages)
total += 3  # Overhead per message
print(f"Input tokens: {total}")
```

### Usage from Response

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

usage = response.usage
print(f"Prompt tokens: {usage.prompt_tokens}")
print(f"Completion tokens: {usage.completion_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Calculate cost
input_cost = usage.prompt_tokens * 2.50 / 1_000_000
output_cost = usage.completion_tokens * 10.00 / 1_000_000
total_cost = input_cost + output_cost
print(f"Cost: ${total_cost:.6f}")
```

### Track Spending

```python
class CostTracker:
    PRICES = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "text-embedding-3-large": {"input": 0.13, "output": 0},
        "dall-e-3-hd-1024": {"per_image": 0.08},
        "whisper-1": {"per_minute": 0.006},
        "tts-1-hd": {"per_char": 0.000030}
    }

    def __init__(self):
        self.total_cost = 0.0
        self.calls = []

    def track_completion(self, model: str, prompt_tokens: int, completion_tokens: int):
        prices = self.PRICES.get(model, {"input": 0, "output": 0})
        cost = (prompt_tokens * prices["input"] + completion_tokens * prices["output"]) / 1_000_000
        self.total_cost += cost
        self.calls.append({"model": model, "cost": cost})
        return cost

    def report(self):
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Total calls: {len(self.calls)}")

tracker = CostTracker()
```

---

## Best Practices

### 1. Model Selection

| Task | Recommended Model | Why |
|------|-------------------|-----|
| General chat | gpt-4o-mini | Cost-effective |
| Complex reasoning | gpt-4o or o1 | Better accuracy |
| Code generation | gpt-4o | Strong coding |
| Quick classification | gpt-4o-mini | Fast, cheap |
| Image generation | dall-e-3 | Best quality |
| Embeddings | text-embedding-3-small | Good balance |

### 2. Prompt Engineering

```python
# Bad
messages = [{"role": "user", "content": "Write something about AI"}]

# Good
messages = [
    {
        "role": "system",
        "content": "You are a technical writer specializing in AI. Write clear, concise content for developers."
    },
    {
        "role": "user",
        "content": """Write a 200-word introduction about AI for a developer audience.

Requirements:
- Focus on practical applications
- Include one code example
- Use simple language"""
    }
]
```

### 3. Caching

```python
import hashlib
import json

class ResponseCache:
    def __init__(self):
        self.cache = {}

    def get_key(self, model: str, messages: list) -> str:
        content = json.dumps({"model": model, "messages": messages}, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, model: str, messages: list):
        key = self.get_key(model, messages)
        return self.cache.get(key)

    def set(self, model: str, messages: list, response):
        key = self.get_key(model, messages)
        self.cache[key] = response

cache = ResponseCache()
```

### 4. Parallel Requests

```python
import asyncio
from openai import AsyncOpenAI

async_client = AsyncOpenAI()

async def parallel_completions(prompts: list[str]) -> list:
    async def get_completion(prompt):
        return await async_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

    return await asyncio.gather(*[get_completion(p) for p in prompts])

# Usage
prompts = ["Hello", "World", "!"]
responses = asyncio.run(parallel_completions(prompts))
```

### 5. Security

```python
# Never log API keys
import logging
logging.getLogger("openai").setLevel(logging.WARNING)

# Validate user input
def sanitize_input(text: str, max_length: int = 10000) -> str:
    if not isinstance(text, str):
        raise ValueError("Input must be string")
    return text[:max_length].strip()

# Use environment variables
import os
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not set")
```

---

## Quick Commands

### curl Examples

```bash
# Chat completion
curl https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Generate image
curl https://api.openai.com/v1/images/generations \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "dall-e-3",
    "prompt": "A robot programming",
    "size": "1024x1024"
  }'

# Transcribe audio
curl https://api.openai.com/v1/audio/transcriptions \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F model="whisper-1" \
  -F file="@speech.mp3"

# Generate speech
curl https://api.openai.com/v1/audio/speech \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "tts-1", "voice": "alloy", "input": "Hello world!"}' \
  --output speech.mp3

# Create embedding
curl https://api.openai.com/v1/embeddings \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "text-embedding-3-small", "input": "Hello world"}'
```

---

## Related Skills

- **faion-claude-api-skill** - Claude API (alternative LLM)
- **faion-gemini-api-skill** - Gemini API (alternative LLM)
- **faion-langchain-skill** - LLM orchestration
- **faion-embeddings-skill** - Vector embeddings
- **faion-image-gen-skill** - Image generation (DALL-E, FLUX, SD)
- **faion-audio-skill** - TTS/STT advanced patterns
- **faion-finetuning-skill** - Model customization

---

## Sources

- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [OpenAI Pricing](https://openai.com/api/pricing/)
- [Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
