---
name: moonshot-ai
version: "1.0.0"
description: Moonshot AI Kimi API - Trillion-parameter MoE model with 256K context, tool calling, and agentic capabilities for chat, coding, and autonomous task execution
---

# Moonshot AI Skill

**Moonshot AI** provides the Kimi large language model series, featuring the flagship **Kimi K2** - a state-of-the-art mixture-of-experts (MoE) model with 1 trillion total parameters. The API offers OpenAI-compatible endpoints with 256K context length, strong tool calling capabilities, and competitive pricing.

**Key Value Proposition**: Access a trillion-parameter model optimized for agentic tasks, tool use, and coding at significantly lower costs than competitors (up to 100x cheaper than GPT-4 for some tasks), with excellent multilingual support for Chinese and English.

## When to Use This Skill

- Integrating Moonshot AI/Kimi models into applications
- Building agentic AI systems with autonomous tool calling
- Processing long documents with 128K-256K context windows
- Developing cost-effective LLM solutions
- Creating multilingual applications (Chinese/English)
- Implementing function calling and tool use patterns

## When NOT to Use This Skill

- For OpenAI API specifically (use openai skill)
- For Claude/Anthropic API (use anthropic skill)
- For image generation or multimodal tasks (Kimi is text-focused)
- For models requiring real-time voice interaction

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    Moonshot AI Platform                          │
│                  platform.moonshot.ai                            │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Kimi K2      │    │ moonshot-v1   │    │   Tool Use    │
│  (Latest)     │    │  (Legacy)     │    │               │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ • 1T params   │    │ • v1-8k       │    │ • Functions   │
│ • 32B active  │    │ • v1-32k      │    │ • Web Search  │
│ • 128K-256K   │    │ • v1-128k     │    │ • Code Exec   │
│ • MoE arch    │    │               │    │ • Custom      │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   API Endpoints   │
                    ├───────────────────┤
                    │ • OpenAI compat   │
                    │ • Anthropic compat│
                    │ • Streaming       │
                    │ • Tool calling    │
                    └───────────────────┘
```

### Model Specifications

| Model | Parameters | Active | Context | Best For |
|-------|------------|--------|---------|----------|
| **kimi-k2-0905-preview** | 1T | 32B | 256K | Latest, agentic tasks |
| **kimi-k2-turbo-preview** | 1T | 32B | 128K | Fast, general use |
| **kimi-k2-thinking** | 1T | 32B | 128K | Multi-step reasoning |
| moonshot-v1-8k | - | - | 8K | Short context |
| moonshot-v1-32k | - | - | 32K | Medium context |
| moonshot-v1-128k | - | - | 128K | Long documents |
| kimi-latest | - | - | Auto | Auto-selects tier |

### Kimi K2 Technical Details

```
Architecture: Mixture-of-Experts (MoE)
Total Parameters: 1 Trillion
Activated Parameters: 32 Billion per token
Layers: 61 (including 1 dense layer)
Experts: 384 total, 8 selected per token
Attention: MLA (Multi-head Latent Attention)
Activation: SwiGLU
Vocabulary: 160K tokens
Context: 128K tokens (256K for 0905-preview)
Training Data: 15.5T tokens
```

---

## Quick Start

### Get API Key

1. Visit [platform.moonshot.ai](https://platform.moonshot.ai)
2. Create an account
3. Generate API key from dashboard

### Environment Setup

```bash
export MOONSHOT_API_KEY="your-api-key-here"

# Optional: Use China endpoint
export MOONSHOT_API_BASE="https://api.moonshot.cn/v1"
```

### Basic Chat Completion

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-api-key",
    base_url="https://api.moonshot.ai/v1"
)

response = client.chat.completions.create(
    model="kimi-k2-0905-preview",
    messages=[
        {"role": "system", "content": "You are Kimi, an AI assistant created by Moonshot AI."},
        {"role": "user", "content": "Explain quantum computing in simple terms."}
    ],
    temperature=0.6,  # Recommended
    max_tokens=1024
)

print(response.choices[0].message.content)
```

---

## API Reference

### Base URLs

| Region | URL |
|--------|-----|
| Global | `https://api.moonshot.ai/v1` |
| China | `https://api.moonshot.cn/v1` |

### Authentication

```bash
curl https://api.moonshot.ai/v1/chat/completions \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2-0905-preview",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Chat Completions

**Endpoint:** `POST /v1/chat/completions`

**Request Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `model` | string | Yes | Model identifier |
| `messages` | array | Yes | Conversation history |
| `temperature` | float | No | 0.0-1.0, recommended 0.6 |
| `max_tokens` | int | No | Maximum response length |
| `stream` | bool | No | Enable streaming |
| `top_p` | float | No | Nucleus sampling |
| `tools` | array | No | Function definitions |
| `tool_choice` | string | No | `auto`, `none`, or specific |

**Message Format:**

```json
{
  "messages": [
    {"role": "system", "content": "System prompt"},
    {"role": "user", "content": "User message"},
    {"role": "assistant", "content": "Previous response"},
    {"role": "user", "content": [
      {"type": "text", "text": "Multimodal content"}
    ]}
  ]
}
```

**Response:**

```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "kimi-k2-0905-preview",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "Response text"
    },
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 100,
    "total_tokens": 150
  }
}
```

---

## Tool Calling / Function Calling

Kimi K2 has strong native support for tool calling, enabling agentic applications.

### Define Tools

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "parameters": {
                "type": "object",
                "required": ["city"],
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    }
                }
            }
        }
    }
]
```

### Make Tool Call Request

```python
response = client.chat.completions.create(
    model="kimi-k2-0905-preview",
    messages=[
        {"role": "user", "content": "What's the weather in Tokyo?"}
    ],
    tools=tools,
    tool_choice="auto",
    temperature=0.6
)

# Check if model wants to call a tool
message = response.choices[0].message
if message.tool_calls:
    for tool_call in message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

### Complete Tool Call Loop

```python
import json

def execute_tool(name: str, args: dict) -> str:
    """Execute tool and return result."""
    if name == "get_weather":
        return json.dumps({"temp": 22, "condition": "sunny"})
    elif name == "search_web":
        return json.dumps({"results": ["Result 1", "Result 2"]})
    return json.dumps({"error": "Unknown tool"})

messages = [{"role": "user", "content": "What's the weather in Tokyo?"}]

while True:
    response = client.chat.completions.create(
        model="kimi-k2-0905-preview",
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.6
    )

    message = response.choices[0].message
    messages.append(message)

    if not message.tool_calls:
        # No more tool calls, done
        print(message.content)
        break

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
```

---

## Streaming

### Python Streaming

```python
stream = client.chat.completions.create(
    model="kimi-k2-0905-preview",
    messages=[{"role": "user", "content": "Write a poem about AI"}],
    stream=True,
    temperature=0.6
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### JavaScript/Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.MOONSHOT_API_KEY,
  baseURL: 'https://api.moonshot.ai/v1'
});

async function chat() {
  const stream = await client.chat.completions.create({
    model: 'kimi-k2-0905-preview',
    messages: [{ role: 'user', content: 'Hello!' }],
    stream: true
  });

  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || '');
  }
}
```

### cURL Streaming

```bash
curl https://api.moonshot.ai/v1/chat/completions \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "kimi-k2-0905-preview",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": true
  }'
```

---

## Pricing

### Kimi K2 Models

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| kimi-k2-0905-preview | ~$0.15 | ~$2.50 |
| kimi-k2-turbo-preview | ~$0.15 | ~$2.50 |

### moonshot-v1 Models (kimi-latest auto-selects)

| Context Tier | Input (per 1M tokens) | Output (per 1M tokens) |
|--------------|----------------------|------------------------|
| 8K | $0.20 | $2.00 |
| 32K | $1.00 | $3.00 |
| 128K | $2.00 | $5.00 |

### Built-in Tools

| Tool | Cost per Call |
|------|---------------|
| $web_search | ~$0.005 |

---

## LiteLLM Integration

### Configuration

```python
from litellm import completion

response = completion(
    model="moonshot/kimi-k2-0905-preview",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Proxy Config (config.yaml)

```yaml
model_list:
  - model_name: kimi-k2
    litellm_params:
      model: moonshot/kimi-k2-0905-preview
      api_key: os.environ/MOONSHOT_API_KEY

  - model_name: kimi-128k
    litellm_params:
      model: moonshot/moonshot-v1-128k
      api_key: os.environ/MOONSHOT_API_KEY
```

### Handled Quirks

LiteLLM automatically handles:
- **Temperature capping**: Values > 1 are clamped
- **Temperature constraint**: Sets to 0.3 when temp < 0.3 and n > 1
- **Tool choice**: Converts "required" by adding context

---

## Anthropic-Compatible API

Moonshot also offers an Anthropic-compatible API endpoint:

```python
from anthropic import Anthropic

client = Anthropic(
    api_key="your-moonshot-key",
    base_url="https://api.moonshot.ai/v1"
)

# Note: Temperature mapping
# real_temperature = request_temperature * 0.6
response = client.messages.create(
    model="kimi-k2-0905-preview",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=1024,
    temperature=1.0  # Will become 0.6 internally
)
```

---

## Best Practices

### Temperature Settings

```python
# Recommended default
temperature = 0.6

# For creative tasks
temperature = 0.8

# For factual/deterministic tasks
temperature = 0.3
```

### System Prompts

```python
# Default system prompt (good starting point)
system_prompt = "You are Kimi, an AI assistant created by Moonshot AI."

# Custom for specific tasks
system_prompt = """You are a coding assistant.
Provide clean, well-documented code with explanations.
Use Python unless otherwise specified."""
```

### Long Context Usage

```python
# For documents up to 256K tokens
response = client.chat.completions.create(
    model="kimi-k2-0905-preview",  # Supports 256K
    messages=[
        {"role": "system", "content": "Analyze the following document."},
        {"role": "user", "content": very_long_document}
    ],
    temperature=0.3  # Lower for analysis tasks
)
```

---

## Performance Benchmarks

| Benchmark | Score | Notes |
|-----------|-------|-------|
| **AIME 2024** | 69.6% | Math reasoning |
| **MATH-500** | 97.4% | Mathematics |
| **LiveCodeBench** | 53.7% | Code generation |
| **SWE-bench Verified** | 71.6% | Agentic coding |
| **MMLU** | 89.5% | General knowledge |
| **MMLU-Redux** | 92.7% | Updated evaluation |
| **Tau2 Retail** | 70.6% | Tool use |
| **AceBench** | 76.5% | Agent evaluation |

---

## Troubleshooting

### Authentication Errors

```
Error: 401 Unauthorized
```

**Solutions:**
1. Verify API key is correct
2. Check environment variable is set
3. Ensure key hasn't expired

### Rate Limiting

```
Error: 429 Too Many Requests
```

**Solutions:**
1. Implement exponential backoff
2. Reduce request frequency
3. Consider upgrading plan

### Context Length Exceeded

```
Error: Context length exceeded
```

**Solutions:**
1. Use longer context model (kimi-k2-0905-preview for 256K)
2. Truncate input text
3. Summarize previous messages

### Tool Call Issues

```
Error: Invalid tool definition
```

**Solutions:**
1. Verify JSON schema is valid
2. Check required fields are present
3. Ensure parameter types are correct

---

## Resources

### Official Documentation
- [Platform](https://platform.moonshot.ai/)
- [API Documentation](https://platform.moonshot.ai/docs/api/chat)
- [Quickstart Guide](https://platform.moonshot.ai/docs/guide/start-using-kimi-api)
- [Tool Use Guide](https://platform.moonshot.ai/docs/api/tool-use)
- [Pricing](https://platform.moonshot.ai/docs/pricing/chat)

### Open Source
- [Kimi K2 GitHub](https://github.com/MoonshotAI/Kimi-K2)
- [Hugging Face Model](https://huggingface.co/moonshotai/Kimi-K2-Instruct)
- [Technical Report](https://github.com/MoonshotAI/Kimi-K2/blob/main/tech_report.pdf)

### Integration Guides
- [LiteLLM Provider](https://docs.litellm.ai/docs/providers/moonshot)

### Support
- Email: support@moonshot.cn

---

## Version History

- **1.0.0** (2026-01-12): Initial skill release
  - Complete Kimi K2 model documentation
  - API reference with all parameters
  - Tool calling / function calling guide
  - Streaming examples (Python, Node.js, cURL)
  - Pricing information
  - LiteLLM and Anthropic-compatible API integration
  - Performance benchmarks
  - Troubleshooting guide
