---
name: xai-models
description: xAI Grok model selection and capabilities guide. Use when choosing the right Grok model for your task, comparing model features, or optimizing costs.
version: 1.0.0
---

# xAI Grok Models Guide

Complete guide to selecting the right Grok model for your use case, with pricing and capability comparisons.

## Model Quick Reference

| Model | Best For | Input $/1M | Output $/1M | Context |
|-------|----------|------------|-------------|---------|
| `grok-4-1-fast` | Tool calling, agents | $0.20 | $0.50 | 2M |
| `grok-4` | Complex reasoning | $3.00 | $15.00 | 256K |
| `grok-3-fast` | General tasks | $0.20 | $0.50 | 131K |
| `grok-3-mini` | Lightweight tasks | $0.30 | $0.50 | 131K |
| `grok-2-vision` | Image analysis | $2.00 | $10.00 | 32K |

## Model Selection Decision Tree

```
What's your primary need?
│
├─► Tool calling / Agent workflows
│   └─► grok-4-1-fast ($0.20/$0.50)
│
├─► Complex reasoning / Analysis
│   └─► grok-4 ($3.00/$15.00)
│
├─► General chat / Simple tasks
│   └─► grok-3-fast ($0.20/$0.50)
│
├─► High volume / Cost sensitive
│   └─► grok-3-mini ($0.30/$0.50)
│
└─► Image/Vision tasks
    └─► grok-2-vision ($2.00/$10.00)
```

## Detailed Model Profiles

### grok-4-1-fast (Recommended for Most Uses)
**Best for:** Tool calling, agentic workflows, real-time search

```python
# Best choice for X search and sentiment analysis
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{"role": "user", "content": "Search X for AAPL sentiment"}]
)
```

**Features:**
- 2 million token context window
- Optimized for tool calling
- Fast response times
- Best price/performance ratio

**Variants:**
- `grok-4-1-fast-reasoning` - Maximum intelligence
- `grok-4-1-fast-non-reasoning` - Instant responses

### grok-4
**Best for:** Deep analysis, complex reasoning, research

```python
# Use for complex multi-step analysis
response = client.chat.completions.create(
    model="grok-4",
    messages=[{"role": "user", "content": "Analyze market trends..."}]
)
```

**Features:**
- Highest reasoning capability
- Best for complex tasks
- 256K context window

### grok-3-fast
**Best for:** General purpose, balanced performance

```python
# Good default choice for most tasks
response = client.chat.completions.create(
    model="grok-3-fast",
    messages=[{"role": "user", "content": "Summarize this..."}]
)
```

**Features:**
- Fast responses
- 131K context
- Good balance of speed/quality

### grok-3-mini
**Best for:** High-volume, cost-sensitive applications

```python
# Use for bulk processing
response = client.chat.completions.create(
    model="grok-3-mini",
    messages=[{"role": "user", "content": "Classify: ..."}]
)
```

**Features:**
- Lowest latency
- Most cost-effective
- Good for simple tasks

### grok-2-vision
**Best for:** Image analysis, charts, screenshots

```python
import base64

# Encode image
with open("chart.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = client.chat.completions.create(
    model="grok-2-vision",
    messages=[{
        "role": "user",
        "content": [
            {"type": "text", "text": "Analyze this chart"},
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}
        ]
    }]
)
```

## Cost Optimization Strategies

### 1. Use the Right Model
```python
# For filtering/classification - use mini
filter_response = client.chat.completions.create(
    model="grok-3-mini",
    messages=[{"role": "user", "content": f"Is this relevant? {text}"}]
)

# For analysis - use fast
if is_relevant:
    analysis = client.chat.completions.create(
        model="grok-4-1-fast",
        messages=[{"role": "user", "content": f"Analyze: {text}"}]
    )
```

### 2. Leverage Caching
Cached input tokens are 75% cheaper:
- Regular: $0.20/1M
- Cached: $0.05/1M

### 3. Batch Similar Requests
```python
# Instead of 10 separate calls, batch them
texts = ["text1", "text2", "text3"]
batch_prompt = "Analyze these texts:\n" + "\n".join(texts)

response = client.chat.completions.create(
    model="grok-3-fast",
    messages=[{"role": "user", "content": batch_prompt}]
)
```

## Tool Calling Costs

| Tool | Cost per 1,000 calls |
|------|---------------------|
| X Search | $5.00 |
| Web Search | $5.00 |
| Code Execution | $5.00 |
| Document Search | $2.50 |

## Context Window Comparison

| Model | Context | Pages of Text | Hours of Audio |
|-------|---------|---------------|----------------|
| grok-4-1-fast | 2M | ~6,000 | ~50 |
| grok-4 | 256K | ~800 | ~6 |
| grok-3-fast | 131K | ~400 | ~3 |
| grok-2-vision | 32K | ~100 | ~1 |

## Model Capabilities Matrix

| Capability | 4.1 Fast | 4 | 3 Fast | 3 Mini | 2 Vision |
|------------|----------|---|--------|--------|----------|
| Tool Calling | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐ | ❌ |
| Reasoning | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐ | ⭐⭐ |
| Speed | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Cost | ⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Vision | ❌ | ❌ | ❌ | ❌ | ⭐⭐⭐ |
| X Search | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ | ❌ |

## Recommended Configurations

### Financial Sentiment Pipeline
```python
MODELS = {
    "filter": "grok-3-mini",      # Fast filtering
    "analyze": "grok-4-1-fast",   # Tool calling + analysis
    "deep": "grok-4"              # Complex reasoning (rare)
}
```

### High-Volume Processing
```python
MODELS = {
    "bulk": "grok-3-mini",
    "quality_check": "grok-3-fast"
}
```

### Research & Analysis
```python
MODELS = {
    "search": "grok-4-1-fast",
    "analyze": "grok-4",
    "summarize": "grok-3-fast"
}
```

## API Usage Example

```python
import os
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("XAI_API_KEY"),
    base_url="https://api.x.ai/v1"
)

# List available models
models = client.models.list()
for model in models.data:
    print(f"{model.id}")

# Use specific model
response = client.chat.completions.create(
    model="grok-4-1-fast",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100
)
```

## Related Skills
- `xai-auth` - Authentication setup
- `xai-agent-tools` - Tool calling
- `xai-sentiment` - Sentiment analysis

## References
- [xAI Models](https://docs.x.ai/docs/models)
- [Pricing](https://docs.x.ai/docs/models)
- [Grok 4.1 Fast Announcement](https://x.ai/news/grok-4-1-fast/)
