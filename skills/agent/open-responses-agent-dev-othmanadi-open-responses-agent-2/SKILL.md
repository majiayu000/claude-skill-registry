---
name: open-responses-agent-dev
description: Build autonomous agents using Open Responses API via HuggingFace Inference Providers. Single unified endpoint with multi-provider routing via model suffixes. Use the OpenAI SDK with custom base_url for seamless development.
---

# Open Responses Agent Development

Build autonomous agents with the **Open Responses API** - the open-source standard for multi-provider, agentic LLM interfaces via HuggingFace Inference Providers.

## When to Use This Skill

Activate this skill when:
- Building autonomous agents (not chatbots)
- Need multi-step workflows in a single request
- Want multi-provider routing with a single endpoint
- Need reasoning visibility (see agent thinking)
- Building sub-agent loops with tools
- Want to use the OpenAI SDK with open-source models

## Key Concept: Single Unified Endpoint

**IMPORTANT:** Open Responses uses ONE unified endpoint with provider routing via model suffixes.

```
Endpoint: https://router.huggingface.co/v1
Model format: model-id:provider (e.g., moonshotai/Kimi-K2-Instruct-0905:groq)
```

Providers are specified as **suffixes** on the model name:
- `:groq` - Groq inference
- `:together` - Together AI
- `:nebius` - Nebius AI
- `:auto` - Automatic provider selection
- (no suffix) - Default provider

---

## Core Concepts

### 1. The Responses Endpoint

```
POST https://router.huggingface.co/v1/responses
Authorization: Bearer $HF_TOKEN
Content-Type: application/json
```

**Request Structure:**
```json
{
  "model": "moonshotai/Kimi-K2-Instruct-0905:groq",
  "instructions": "You are a helpful assistant.",
  "input": "User request",
  "tools": [...],
  "tool_choice": "auto",
  "reasoning": { "effort": "medium" },
  "stream": false
}
```

**Response Structure:**
```json
{
  "id": "resp_abc123",
  "model": "moonshotai/Kimi-K2-Instruct-0905:groq",
  "output": [
    { "type": "reasoning", "content": "Let me think..." },
    { "type": "function_call", "name": "search", "arguments": "{...}" },
    { "type": "function_call_output", "output": "..." },
    { "type": "message", "content": "Final response" }
  ],
  "output_text": "Final response",
  "usage": { "input_tokens": 100, "output_tokens": 200 }
}
```

### 2. Sub-Agent Loops

The API automatically handles:
1. Model samples a response
2. Emits tool calls if needed
3. Executes tools (for server-side tools like MCP)
4. Feeds results back
5. Repeats until completion

**No manual loop management required!**

### 3. Reasoning Visibility

Three fields for reasoning:
- `content`: Raw reasoning traces (open weight models)
- `encrypted_content`: Protected reasoning (proprietary models)
- `summary`: Sanitized summary

Control reasoning effort:
```json
{ "reasoning": { "effort": "low" | "medium" | "high" } }
```

### 4. Semantic Streaming

Events are structured, not raw text:
```
event: response.created
event: response.output_item.added
event: response.output_text.delta
event: response.output_item.done
event: response.completed
```

---

## Language Selection

Choose based on your use case:

| Language | Best For | Recommended SDK |
|----------|----------|-----------------|
| **TypeScript** | Web apps, serverless, Node.js | `openai` npm package |
| **Python** | ML/AI, data science, rapid prototyping | `openai` pip package |

---

## TypeScript Implementation

### Setup

```bash
npm init -y
npm install openai
```

### Basic Agent (Using OpenAI SDK)

```typescript
import OpenAI from "openai";

// Configure client with HuggingFace router
const client = new OpenAI({
  baseURL: "https://router.huggingface.co/v1",
  apiKey: process.env.HF_TOKEN,
});

async function createAgent(
  model: string,
  input: string,
  instructions?: string
) {
  const response = await client.responses.create({
    model,  // e.g., "moonshotai/Kimi-K2-Instruct-0905:groq"
    instructions: instructions || "You are a helpful assistant.",
    input,
  });

  // Use the convenience helper for simple text output
  console.log(response.output_text);

  // Or iterate through all output items
  for (const item of response.output) {
    console.log(item.type, item.content);
  }

  return response;
}

// Usage
const result = await createAgent(
  "moonshotai/Kimi-K2-Instruct-0905:groq",
  "What is the capital of France?"
);
```

### Sub-Agent Loop with Tools

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://router.huggingface.co/v1",
  apiKey: process.env.HF_TOKEN,
});

// Tools are defined at top level (not nested in function object)
const tools = [
  {
    type: "function" as const,
    name: "get_current_weather",
    description: "Get the current weather in a given location",
    parameters: {
      type: "object",
      properties: {
        location: { type: "string", description: "City and state, e.g. San Francisco, CA" },
        unit: { type: "string", enum: ["celsius", "fahrenheit"] },
      },
      required: ["location", "unit"],
    },
  },
  {
    type: "function" as const,
    name: "search_documents",
    description: "Search company documents for information",
    parameters: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
      },
      required: ["query"],
    },
  },
];

async function runAgentWithTools() {
  const response = await client.responses.create({
    model: "moonshotai/Kimi-K2-Instruct-0905:groq",
    instructions: "You are a helpful assistant.",
    input: "What is the weather like in Boston today?",
    tools,
    tool_choice: "auto",
  });

  // Process all output items
  for (const item of response.output) {
    switch (item.type) {
      case "reasoning":
        console.log(`[REASONING] ${item.content}`);
        break;
      case "function_call":
        console.log(`[TOOL CALL] ${item.name}(${JSON.stringify(item.arguments)})`);
        break;
      case "function_call_output":
        console.log(`[TOOL RESULT] ${item.output}`);
        break;
      case "message":
        console.log(`[RESPONSE] ${item.content}`);
        break;
    }
  }

  return response;
}
```

### Streaming (TypeScript)

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://router.huggingface.co/v1",
  apiKey: process.env.HF_TOKEN,
});

async function streamAgent() {
  const stream = await client.responses.create({
    model: "moonshotai/Kimi-K2-Instruct-0905:groq",
    instructions: "You are a helpful assistant.",
    input: "Say 'double bubble bath' ten times fast.",
    stream: true,
  });

  for await (const event of stream) {
    console.log(event);
  }
}
```

### Structured Outputs

```typescript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "https://router.huggingface.co/v1",
  apiKey: process.env.HF_TOKEN,
});

async function getStructuredOutput() {
  const response = await client.responses.create({
    model: "openai/gpt-oss-120b:groq",
    instructions: "Extract the event information. Return JSON.",
    input: "Alice and Bob are going to a science fair on Friday.",
    response_format: {
      type: "json_schema",
      json_schema: {
        name: "CalendarEvent",
        schema: {
          type: "object",
          properties: {
            name: { type: "string" },
            date: { type: "string" },
            participants: { type: "array", items: { type: "string" } },
          },
          required: ["name", "date", "participants"],
          additionalProperties: false,
        },
        strict: true,
      },
    },
  });

  const parsed = JSON.parse(response.output_text);
  console.log(parsed);
}
```

---

## Python Implementation

### Setup

```bash
pip install openai
```

### Basic Agent (Using OpenAI SDK)

```python
import os
from openai import OpenAI

# Configure client with HuggingFace router
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def create_agent(model: str, input_text: str, instructions: str = None):
    response = client.responses.create(
        model=model,  # e.g., "moonshotai/Kimi-K2-Instruct-0905:groq"
        instructions=instructions or "You are a helpful assistant.",
        input=input_text,
    )

    # Use the convenience helper for simple text output
    print(response.output_text)

    # Or iterate through all output items
    for item in response.output:
        print(item.type, item.content)

    return response

# Usage
result = create_agent(
    "moonshotai/Kimi-K2-Instruct-0905:groq",
    "What is the capital of France?"
)
```

### Sub-Agent Loop with Tools

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

# Tools are defined at top level (not nested in function object)
tools = [
    {
        "type": "function",
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City and state, e.g. San Francisco, CA"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location", "unit"],
        },
    },
    {
        "type": "function",
        "name": "search_documents",
        "description": "Search company documents for information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
    },
]

def run_agent_with_tools():
    response = client.responses.create(
        model="moonshotai/Kimi-K2-Instruct-0905:groq",
        instructions="You are a helpful assistant.",
        input="What is the weather like in Boston today?",
        tools=tools,
        tool_choice="auto",
    )

    # Process all output items
    for item in response.output:
        match item.type:
            case "reasoning":
                print(f"[REASONING] {item.content}")
            case "function_call":
                print(f"[TOOL CALL] {item.name}({item.arguments})")
            case "function_call_output":
                print(f"[TOOL RESULT] {item.output}")
            case "message":
                print(f"[RESPONSE] {item.content}")

    return response

run_agent_with_tools()
```

### Streaming (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def stream_agent():
    stream = client.responses.create(
        model="moonshotai/Kimi-K2-Instruct-0905:groq",
        input=[{"role": "user", "content": "Say 'double bubble bath' ten times fast."}],
        stream=True,
    )

    for event in stream:
        print(event)

stream_agent()
```

### Structured Outputs (Python)

```python
import os
from openai import OpenAI
from pydantic import BaseModel

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

def get_structured_output():
    response = client.responses.parse(
        model="openai/gpt-oss-120b:groq",
        input=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
        ],
        text_format=CalendarEvent,
    )

    print(response.output_parsed)

get_structured_output()
```

### Reasoning Control (Python)

```python
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

def agent_with_reasoning():
    response = client.responses.create(
        model="openai/gpt-oss-120b:groq",
        instructions="You are a helpful assistant.",
        input="Say hello to the world.",
        reasoning={"effort": "low"},  # "low" | "medium" | "high"
    )

    for i, item in enumerate(response.output):
        print(f"Output #{i}: {item.type}", item.content)

agent_with_reasoning()
```

---

## Provider Routing

Switch providers by changing the model suffix:

```python
# Same endpoint, different providers via model suffix
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.getenv("HF_TOKEN"),
)

# Use Groq
response = client.responses.create(model="moonshotai/Kimi-K2-Instruct-0905:groq", ...)

# Use Together AI
response = client.responses.create(model="meta-llama/Llama-3.1-70B-Instruct:together", ...)

# Use Nebius
response = client.responses.create(model="meta-llama/Llama-3.1-70B-Instruct:nebius", ...)

# Auto-select provider
response = client.responses.create(model="meta-llama/Llama-3.1-70B-Instruct:auto", ...)
```

---

## Available Providers (via Model Suffix)

| Suffix | Provider | Reasoning |
|--------|----------|-----------|
| `:groq` | Groq | Fast inference |
| `:together` | Together AI | Open weight models |
| `:nebius` | Nebius AI | European infrastructure |
| `:auto` | Automatic | System chooses |
| (none) | Default | Provider default |

Browse available models: [HuggingFace Inference Models](https://huggingface.co/inference/models)

---

## Migration from Chat Completion

### Before (Chat Completion - Manual Loop)

```typescript
// OLD: Manual agentic loop with OpenAI client
const openai = new OpenAI();
let messages = [{ role: "user", content: "Search and summarize" }];

while (true) {
  const response = await openai.chat.completions.create({
    model: "gpt-4",
    messages,
    tools,
  });

  if (response.choices[0].finish_reason === "tool_calls") {
    // Manually execute tools
    // Manually manage state
    // Loop again...
  } else {
    break;
  }
}
```

### After (Open Responses - Single Request)

```typescript
// NEW: Single request, automatic loop
const client = new OpenAI({
  baseURL: "https://router.huggingface.co/v1",
  apiKey: process.env.HF_TOKEN,
});

const response = await client.responses.create({
  model: "moonshotai/Kimi-K2-Instruct-0905:groq",
  instructions: "You are a helpful assistant.",
  input: "Search and summarize",
  tools,
  tool_choice: "auto",
});

// Complete execution trace in response.output
for (const item of response.output) {
  console.log(item);
}
```

---

## Best Practices

### 1. Use the OpenAI SDK
```python
# Recommended: Use official SDK with custom base_url
from openai import OpenAI
client = OpenAI(base_url="https://router.huggingface.co/v1", api_key=token)
```

### 2. Include Provider Suffix
```python
# Be explicit about provider for consistency
model = "moonshotai/Kimi-K2-Instruct-0905:groq"
```

### 3. Use instructions Field
```python
response = client.responses.create(
    model="...",
    instructions="You are a helpful assistant.",  # System prompt
    input="User message",
)
```

### 4. Handle All Output Types
```python
for item in response.output:
    match item.type:
        case "reasoning": ...
        case "function_call": ...
        case "function_call_output": ...
        case "message": ...
```

### 5. Use output_text for Simple Cases
```python
# Quick access to final text response
print(response.output_text)
```

### 6. Control Reasoning Effort
```python
response = client.responses.create(
    model="...",
    reasoning={"effort": "medium"},  # low, medium, high
    ...
)
```

---

## Resources

- **HuggingFace Docs:** [huggingface.co/docs/inference-providers/en/guides/responses-api](https://huggingface.co/docs/inference-providers/en/guides/responses-api)
- **Open Responses Spec:** [openresponses.org/specification](https://openresponses.org/specification)
- **GitHub:** [github.com/openresponses/openresponses](https://github.com/openresponses/openresponses)
- **HuggingFace Blog:** [huggingface.co/blog/open-responses](https://huggingface.co/blog/open-responses)
- **Available Models:** [huggingface.co/inference/models](https://huggingface.co/inference/models)

---

## Examples

See the `/examples` directory for complete implementations:
- `examples/typescript/` - TypeScript examples
- `examples/python/` - Python examples

## Templates

See the `/templates` directory for starter code:
- `templates/typescript/agent-template.ts`
- `templates/python/agent_template.py`
