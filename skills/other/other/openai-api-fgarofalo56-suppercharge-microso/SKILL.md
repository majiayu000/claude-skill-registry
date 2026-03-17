---
name: openai-api
description: Build with OpenAI APIs including GPT-4, GPT-4o, function calling, embeddings, vision, and Assistants. Covers chat completions, structured outputs, streaming, and token optimization. Use when integrating OpenAI models into applications.
---

# OpenAI API Skill

> Build production-ready applications with OpenAI's GPT-4, GPT-4o, embeddings, vision, and Assistants API.

## Quick Reference

| Feature            | Model                            | Use Case                       |
| ------------------ | -------------------------------- | ------------------------------ |
| Chat Completions   | `gpt-4o`, `gpt-4-turbo`          | Conversations, reasoning       |
| Structured Outputs | `gpt-4o-2024-08-06+`             | JSON schemas, typed responses  |
| Function Calling   | `gpt-4o`, `gpt-4-turbo`          | Tool use, API integration      |
| Vision             | `gpt-4o`, `gpt-4-vision-preview` | Image analysis                 |
| Embeddings         | `text-embedding-3-small/large`   | Semantic search, RAG           |
| Assistants         | `gpt-4o`, `gpt-4-turbo`          | Stateful agents, file handling |

---

## Installation

```bash
# Python
pip install openai

# Node.js / TypeScript
npm install openai
```

### Client Setup

**Python:**

```python
from openai import OpenAI

# Uses OPENAI_API_KEY env var by default
client = OpenAI()

# Or explicit key
client = OpenAI(api_key="sk-...")
```

**TypeScript:**

```typescript
import OpenAI from "openai";

const openai = new OpenAI(); // Uses OPENAI_API_KEY env var
// Or: new OpenAI({ apiKey: 'sk-...' })
```

---

## Chat Completions

### Basic Chat

**Python:**

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain async/await in Python"}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

**TypeScript:**

```typescript
const response = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [
    { role: "system", content: "You are a helpful assistant." },
    { role: "user", content: "Explain async/await in TypeScript" },
  ],
  temperature: 0.7,
  max_tokens: 500,
});

console.log(response.choices[0].message.content);
```

### Multi-Turn Conversation

```python
conversation = [
    {"role": "system", "content": "You are a Python tutor."}
]

def chat(user_message: str) -> str:
    conversation.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=conversation
    )

    assistant_message = response.choices[0].message.content
    conversation.append({"role": "assistant", "content": assistant_message})

    return assistant_message
```

### Model Selection Guide

| Model           | Context | Best For                | Cost |
| --------------- | ------- | ----------------------- | ---- |
| `gpt-4o`        | 128K    | General purpose, vision | $$   |
| `gpt-4o-mini`   | 128K    | Fast, cost-effective    | $    |
| `gpt-4-turbo`   | 128K    | Complex reasoning       | $$$  |
| `gpt-3.5-turbo` | 16K     | Simple tasks            | $    |

---

## Structured Outputs / JSON Mode

### JSON Mode (Legacy)

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Output valid JSON only."},
        {"role": "user", "content": "List 3 programming languages with their use cases"}
    ],
    response_format={"type": "json_object"}
)

import json
data = json.loads(response.choices[0].message.content)
```

### Structured Outputs with JSON Schema (Recommended)

**Python with Pydantic:**

```python
from pydantic import BaseModel
from typing import List

class Language(BaseModel):
    name: str
    use_cases: List[str]
    difficulty: str

class LanguageList(BaseModel):
    languages: List[Language]

response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "user", "content": "List 3 programming languages"}
    ],
    response_format=LanguageList
)

# Typed response
languages: LanguageList = response.choices[0].message.parsed
for lang in languages.languages:
    print(f"{lang.name}: {lang.difficulty}")
```

**TypeScript with Zod:**

```typescript
import { z } from "zod";
import { zodResponseFormat } from "openai/helpers/zod";

const LanguageSchema = z.object({
  languages: z.array(
    z.object({
      name: z.string(),
      use_cases: z.array(z.string()),
      difficulty: z.enum(["beginner", "intermediate", "advanced"]),
    }),
  ),
});

const response = await openai.beta.chat.completions.parse({
  model: "gpt-4o-2024-08-06",
  messages: [{ role: "user", content: "List 3 programming languages" }],
  response_format: zodResponseFormat(LanguageSchema, "languages"),
});

const languages = response.choices[0].message.parsed;
```

---

## Function Calling / Tools

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
                        "description": "City and state, e.g., San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "default": "fahrenheit"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_database",
            "description": "Search products in database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "limit": {"type": "integer", "default": 10}
                },
                "required": ["query"]
            }
        }
    }
]
```

### Execute Tool Calls

```python
import json

def execute_tool(name: str, args: dict) -> str:
    """Execute tool and return result as string."""
    if name == "get_weather":
        # Call actual weather API
        return json.dumps({"temp": 72, "condition": "sunny"})
    elif name == "search_database":
        # Query database
        return json.dumps({"results": ["Product A", "Product B"]})
    return json.dumps({"error": "Unknown tool"})

def chat_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # or "required" to force tool use
    )

    message = response.choices[0].message

    # Check if model wants to call tools
    if message.tool_calls:
        messages.append(message)  # Add assistant message with tool calls

        # Execute each tool call
        for tool_call in message.tool_calls:
            result = execute_tool(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        # Get final response with tool results
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools
        )
        return final_response.choices[0].message.content

    return message.content
```

### Parallel Tool Calls

```python
# Model can call multiple tools in parallel
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in NYC and LA?"}],
    tools=tools,
    parallel_tool_calls=True  # Default is True
)

# Process all tool calls
for tool_call in response.choices[0].message.tool_calls:
    print(f"Tool: {tool_call.function.name}")
    print(f"Args: {tool_call.function.arguments}")
```

---

## Vision (Image Inputs)

### Analyze Images

**Python:**

```python
import base64

def encode_image(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

# From URL
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {"url": "https://example.com/image.jpg"}
            }
        ]
    }]
)

# From base64
image_data = encode_image("screenshot.png")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this UI screenshot"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{image_data}",
                    "detail": "high"  # "low", "high", or "auto"
                }
            }
        ]
    }]
)
```

### Multiple Images

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Compare these two images"},
            {"type": "image_url", "image_url": {"url": "https://example.com/before.jpg"}},
            {"type": "image_url", "image_url": {"url": "https://example.com/after.jpg"}}
        ]
    }]
)
```

---

## Embeddings

### Generate Embeddings

**Python:**

```python
def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding

# Single text
embedding = get_embedding("OpenAI makes great APIs")
print(f"Dimensions: {len(embedding)}")  # 1536 for small, 3072 for large

# Batch embeddings (more efficient)
texts = ["First document", "Second document", "Third document"]
response = client.embeddings.create(
    input=texts,
    model="text-embedding-3-small"
)
embeddings = [item.embedding for item in response.data]
```

### Reduced Dimensions

```python
# Use dimensions parameter for smaller embeddings
response = client.embeddings.create(
    input="Sample text",
    model="text-embedding-3-large",
    dimensions=256  # Reduce from 3072 to 256
)
```

### Semantic Search Example

```python
import numpy as np
from typing import List, Tuple

def cosine_similarity(a: List[float], b: List[float]) -> float:
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_search(query: str, documents: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    query_embedding = get_embedding(query)
    doc_embeddings = [get_embedding(doc) for doc in documents]

    similarities = [
        (doc, cosine_similarity(query_embedding, emb))
        for doc, emb in zip(documents, doc_embeddings)
    ]

    return sorted(similarities, key=lambda x: x[1], reverse=True)[:top_k]
```

---

## Streaming Responses

### Basic Streaming

**Python:**

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Write a short story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

**TypeScript:**

```typescript
const stream = await openai.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Write a short story" }],
  stream: true,
});

for await (const chunk of stream) {
  const content = chunk.choices[0]?.delta?.content;
  if (content) process.stdout.write(content);
}
```

### Streaming with Tools

```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=tools,
    stream=True
)

tool_calls = []
current_tool = None

for chunk in stream:
    delta = chunk.choices[0].delta

    if delta.tool_calls:
        for tc in delta.tool_calls:
            if tc.index >= len(tool_calls):
                tool_calls.append({
                    "id": tc.id,
                    "function": {"name": tc.function.name, "arguments": ""}
                })
            if tc.function.arguments:
                tool_calls[tc.index]["function"]["arguments"] += tc.function.arguments

    if delta.content:
        print(delta.content, end="", flush=True)
```

---

## Assistants API

### Create an Assistant

```python
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You are a data analyst. Analyze data and create visualizations.",
    model="gpt-4o",
    tools=[
        {"type": "code_interpreter"},
        {"type": "file_search"}
    ]
)
```

### Run a Conversation

```python
# Create thread
thread = client.beta.threads.create()

# Add message
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Analyze this CSV and create a chart"
)

# Run assistant
run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id,
    assistant_id=assistant.id
)

if run.status == "completed":
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages.data:
        if msg.role == "assistant":
            print(msg.content[0].text.value)
```

### File Handling

```python
# Upload file
file = client.files.create(
    file=open("data.csv", "rb"),
    purpose="assistants"
)

# Create vector store for file search
vector_store = client.beta.vector_stores.create(name="Knowledge Base")
client.beta.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id
)

# Attach to assistant
client.beta.assistants.update(
    assistant_id=assistant.id,
    tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
)
```

---

## Token Management & Cost Optimization

### Count Tokens

```python
import tiktoken

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def count_message_tokens(messages: list, model: str = "gpt-4o") -> int:
    encoding = tiktoken.encoding_for_model(model)
    tokens = 0
    for msg in messages:
        tokens += 4  # Message overhead
        tokens += len(encoding.encode(msg["content"]))
    tokens += 2  # Reply priming
    return tokens
```

### Optimize Context

```python
def truncate_to_token_limit(text: str, max_tokens: int, model: str = "gpt-4o") -> str:
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(text)
    if len(tokens) <= max_tokens:
        return text
    return encoding.decode(tokens[:max_tokens])

def manage_conversation_context(
    messages: list,
    max_context_tokens: int = 8000,
    model: str = "gpt-4o"
) -> list:
    """Keep conversation under token limit by removing old messages."""
    while count_message_tokens(messages, model) > max_context_tokens:
        # Keep system message, remove oldest user/assistant pair
        if len(messages) > 3:
            messages.pop(1)
            messages.pop(1)
        else:
            break
    return messages
```

### Cost Tracking

```python
# Pricing per 1M tokens (as of 2024)
PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "text-embedding-3-small": {"input": 0.02},
    "text-embedding-3-large": {"input": 0.13}
}

def calculate_cost(
    model: str,
    input_tokens: int,
    output_tokens: int = 0
) -> float:
    pricing = PRICING.get(model, {})
    input_cost = (input_tokens / 1_000_000) * pricing.get("input", 0)
    output_cost = (output_tokens / 1_000_000) * pricing.get("output", 0)
    return input_cost + output_cost

# Track usage from response
response = client.chat.completions.create(...)
usage = response.usage
cost = calculate_cost(
    "gpt-4o",
    usage.prompt_tokens,
    usage.completion_tokens
)
print(f"Cost: ${cost:.4f}")
```

---

## Error Handling & Retries

### Retry with Exponential Backoff

```python
import time
from openai import RateLimitError, APITimeoutError, APIConnectionError

def chat_with_retry(
    messages: list,
    model: str = "gpt-4o",
    max_retries: int = 3,
    base_delay: float = 1.0
) -> str:
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)

        except (APITimeoutError, APIConnectionError) as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Connection error. Retrying in {delay}s...")
            time.sleep(delay)

    raise Exception("Max retries exceeded")
```

### Using Tenacity

```python
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)
from openai import RateLimitError, APITimeoutError

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    retry=retry_if_exception_type((RateLimitError, APITimeoutError))
)
def robust_chat(messages: list, model: str = "gpt-4o") -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content
```

### Handle All Errors

```python
from openai import (
    OpenAIError,
    APIError,
    AuthenticationError,
    BadRequestError,
    RateLimitError
)

try:
    response = client.chat.completions.create(...)
except AuthenticationError:
    print("Invalid API key")
except BadRequestError as e:
    print(f"Invalid request: {e.message}")
except RateLimitError:
    print("Rate limited - implement backoff")
except APIError as e:
    print(f"API error: {e.status_code} - {e.message}")
except OpenAIError as e:
    print(f"OpenAI error: {e}")
```

---

## Best Practices

### System Prompt Design

```python
SYSTEM_PROMPT = """You are a helpful assistant for {company_name}.

## Your Role
- Answer questions about our products
- Help troubleshoot issues
- Escalate complex problems to human support

## Guidelines
- Be concise and direct
- Use bullet points for lists
- If unsure, say so honestly
- Never make up information

## Tone
- Professional but friendly
- Patient with confused users
- Empathetic to frustrations
"""
```

### Prompt Templates

```python
from string import Template

ANALYSIS_TEMPLATE = Template("""
Analyze the following $content_type:

---
$content
---

Provide:
1. Summary (2-3 sentences)
2. Key points (bullet list)
3. Recommendations (if applicable)
""")

prompt = ANALYSIS_TEMPLATE.substitute(
    content_type="customer feedback",
    content="The product is great but shipping was slow..."
)
```

### Production Checklist

| Category        | Recommendation                        |
| --------------- | ------------------------------------- |
| **Security**    | Never expose API keys; use env vars   |
| **Rate Limits** | Implement exponential backoff         |
| **Costs**       | Set usage limits; monitor daily spend |
| **Latency**     | Use streaming for long responses      |
| **Reliability** | Add fallback models (4o → 4o-mini)    |
| **Logging**     | Log prompts, responses, tokens, costs |
| **Testing**     | Test with edge cases; mock in tests   |

### Fallback Pattern

```python
MODELS = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]

def chat_with_fallback(messages: list) -> str:
    for model in MODELS:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                timeout=30
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"{model} failed: {e}")
            continue
    raise Exception("All models failed")
```

---

## Quick Patterns

### Simple Q&A

```python
def ask(question: str) -> str:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    ).choices[0].message.content
```

### Summarize Text

```python
def summarize(text: str, max_words: int = 100) -> str:
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"Summarize in {max_words} words:\n\n{text}"
        }]
    ).choices[0].message.content
```

### Extract Structured Data

```python
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    email: str | None
    phone: str | None

def extract_contact(text: str) -> Contact:
    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[{
            "role": "user",
            "content": f"Extract contact info:\n\n{text}"
        }],
        response_format=Contact
    )
    return response.choices[0].message.parsed
```

---

## Resources

- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OpenAI Cookbook](https://cookbook.openai.com/)
- [Pricing](https://openai.com/pricing)
- [Rate Limits](https://platform.openai.com/docs/guides/rate-limits)
- [Tiktoken Tokenizer](https://github.com/openai/tiktoken)
