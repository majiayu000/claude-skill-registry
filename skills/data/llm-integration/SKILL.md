---
name: llm-integration
description: "Use when integrating LLM APIs into applications. Covers API patterns, prompt templates, streaming, error handling, cost optimization, and provider abstraction. Apply when building chat interfaces, completion endpoints, or AI-powered features."
---

# LLM Integration

## Core Principle

Treat LLM calls like any external API: handle errors, implement retries, monitor costs, and abstract the provider.

## When to Use This Skill

- Integrating OpenAI, Anthropic, or other LLM APIs
- Building chat interfaces or completion features
- Implementing streaming responses
- Optimizing API costs
- Handling rate limits and errors
- Creating provider-agnostic abstractions

## The Iron Law

**NEVER TRUST LLM OUTPUT BLINDLY.**

Always validate, sanitize, and handle malformed responses.

## Why This Matters?

**Benefits:**
- Reliable AI features in production
- Predictable costs
- Good user experience
- Easy provider switching
- Maintainable codebase

**Without proper integration:**
- Silent failures
- Cost explosions
- Poor UX (slow, broken)
- Vendor lock-in
- Technical debt

## API Client Setup

### OpenAI

```python
from openai import OpenAI

# Initialize client
client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    timeout=30.0,
    max_retries=3,
)

# Basic completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000,
)

print(response.choices[0].message.content)
```

### Anthropic

```python
from anthropic import Anthropic

client = Anthropic(
    api_key=os.environ["ANTHROPIC_API_KEY"],
)

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.content[0].text)
```

### Provider Abstraction

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Message:
    role: str  # "system", "user", "assistant"
    content: str

@dataclass
class LLMResponse:
    content: str
    model: str
    tokens_used: int
    cost_usd: float
    finish_reason: str

class LLMProvider(ABC):
    @abstractmethod
    def complete(
        self,
        messages: List[Message],
        **kwargs
    ) -> LLMResponse:
        pass

    @abstractmethod
    def stream(
        self,
        messages: List[Message],
        **kwargs
    ):
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, model="gpt-4o"):
        self.client = OpenAI()
        self.model = model
        self.pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        }

    def complete(self, messages, **kwargs):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": m.role, "content": m.content} for m in messages],
            **kwargs
        )

        usage = response.usage
        cost = self._calculate_cost(usage.prompt_tokens, usage.completion_tokens)

        return LLMResponse(
            content=response.choices[0].message.content,
            model=self.model,
            tokens_used=usage.total_tokens,
            cost_usd=cost,
            finish_reason=response.choices[0].finish_reason,
        )

    def _calculate_cost(self, input_tokens, output_tokens):
        pricing = self.pricing.get(self.model, {"input": 0, "output": 0})
        return (
            (input_tokens / 1_000_000) * pricing["input"] +
            (output_tokens / 1_000_000) * pricing["output"]
        )

class AnthropicProvider(LLMProvider):
    def __init__(self, model="claude-sonnet-4-20250514"):
        self.client = Anthropic()
        self.model = model
        self.pricing = {
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
            "claude-haiku-4-20250514": {"input": 0.25, "output": 1.25},
        }

    def complete(self, messages, **kwargs):
        # Extract system message
        system = None
        chat_messages = []
        for m in messages:
            if m.role == "system":
                system = m.content
            else:
                chat_messages.append({"role": m.role, "content": m.content})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=kwargs.get("max_tokens", 1024),
            system=system,
            messages=chat_messages,
        )

        cost = self._calculate_cost(
            response.usage.input_tokens,
            response.usage.output_tokens
        )

        return LLMResponse(
            content=response.content[0].text,
            model=self.model,
            tokens_used=response.usage.input_tokens + response.usage.output_tokens,
            cost_usd=cost,
            finish_reason=response.stop_reason,
        )
```

## Streaming Responses

### OpenAI Streaming

```python
def stream_openai(messages):
    """Stream response for better UX."""
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Usage
for text in stream_openai(messages):
    print(text, end="", flush=True)
```

### Anthropic Streaming

```python
def stream_anthropic(messages):
    """Stream Anthropic response."""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=messages,
    ) as stream:
        for text in stream.text_stream:
            yield text
```

### Server-Sent Events (SSE) for Web

```python
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    async def generate():
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=request.messages,
            stream=True,
        )

        for chunk in stream:
            if content := chunk.choices[0].delta.content:
                yield f"data: {json.dumps({'content': content})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )
```

## Prompt Templates

### Simple Templates

```python
from string import Template

SUMMARY_PROMPT = Template("""
Summarize the following text in $num_sentences sentences:

$text

Summary:
""")

prompt = SUMMARY_PROMPT.substitute(
    num_sentences=3,
    text="Long article here..."
)
```

### Structured Prompts with Jinja2

```python
from jinja2 import Template

ANALYSIS_PROMPT = Template("""
You are a {{ role }}.

Analyze the following {{ content_type }}:

{{ content }}

{% if criteria %}
Evaluate based on these criteria:
{% for criterion in criteria %}
- {{ criterion }}
{% endfor %}
{% endif %}

Provide your analysis in {{ format }} format.
""")

prompt = ANALYSIS_PROMPT.render(
    role="senior code reviewer",
    content_type="pull request",
    content=pr_diff,
    criteria=["correctness", "performance", "security"],
    format="JSON"
)
```

### Few-Shot Prompts

```python
def create_few_shot_prompt(task, examples, query):
    """Create few-shot prompt with examples."""
    prompt = f"Task: {task}\n\n"

    for i, ex in enumerate(examples, 1):
        prompt += f"Example {i}:\n"
        prompt += f"Input: {ex['input']}\n"
        prompt += f"Output: {ex['output']}\n\n"

    prompt += f"Now process:\nInput: {query}\nOutput:"

    return prompt

# Usage
examples = [
    {"input": "The food was great!", "output": "positive"},
    {"input": "Terrible service.", "output": "negative"},
]

prompt = create_few_shot_prompt(
    task="Classify the sentiment of the text.",
    examples=examples,
    query="I love this product!"
)
```

## Structured Output

### JSON Mode (OpenAI)

```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "Extract entities. Respond in JSON format."
        },
        {
            "role": "user",
            "content": "John works at Google in New York."
        }
    ],
    response_format={"type": "json_object"}
)

data = json.loads(response.choices[0].message.content)
# {"entities": [{"name": "John", "type": "person"}, ...]}
```

### Structured Output with Pydantic

```python
from pydantic import BaseModel
from typing import List

class Entity(BaseModel):
    name: str
    type: str
    confidence: float

class ExtractionResult(BaseModel):
    entities: List[Entity]
    summary: str

# OpenAI with structured output
response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[...],
    response_format=ExtractionResult,
)

result: ExtractionResult = response.choices[0].message.parsed
```

### Tool/Function Calling

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
                        "description": "City name"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "What's the weather in Paris?"}
    ],
    tools=tools,
    tool_choice="auto"
)

if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    arguments = json.loads(tool_call.function.arguments)

    # Execute function
    result = get_weather(**arguments)

    # Continue conversation with result
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(result)
    })
```

## Error Handling

### Comprehensive Error Handler

```python
from openai import (
    APIError,
    APIConnectionError,
    RateLimitError,
    AuthenticationError,
)
import time
from functools import wraps

def with_retries(max_retries=3, backoff_factor=2):
    """Decorator for LLM calls with retry logic."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)

                except RateLimitError as e:
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    last_exception = e

                except APIConnectionError as e:
                    wait_time = backoff_factor ** attempt
                    logger.warning(f"Connection error. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    last_exception = e

                except AuthenticationError as e:
                    logger.error("Authentication failed. Check API key.")
                    raise

                except APIError as e:
                    if e.status_code >= 500:
                        # Server error, retry
                        wait_time = backoff_factor ** attempt
                        time.sleep(wait_time)
                        last_exception = e
                    else:
                        # Client error, don't retry
                        raise

            raise last_exception

        return wrapper
    return decorator

@with_retries(max_retries=3)
def call_llm(messages):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages
    )
```

### Timeout Handling

```python
import asyncio
from asyncio import timeout

async def call_with_timeout(messages, timeout_seconds=30):
    """Call LLM with timeout."""
    try:
        async with timeout(timeout_seconds):
            response = await async_client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return response
    except asyncio.TimeoutError:
        logger.error(f"LLM call timed out after {timeout_seconds}s")
        raise
```

### Fallback Chain

```python
class FallbackChain:
    """Try multiple providers in order."""

    def __init__(self, providers):
        self.providers = providers

    def complete(self, messages, **kwargs):
        errors = []

        for provider in self.providers:
            try:
                return provider.complete(messages, **kwargs)
            except Exception as e:
                errors.append((provider.__class__.__name__, str(e)))
                continue

        raise AllProvidersFailed(errors)

# Usage
chain = FallbackChain([
    OpenAIProvider(model="gpt-4o"),
    AnthropicProvider(model="claude-sonnet-4-20250514"),
    OpenAIProvider(model="gpt-4o-mini"),  # Cheaper fallback
])

response = chain.complete(messages)
```

## Cost Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text, model="gpt-4o"):
    """Count tokens for cost estimation."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def estimate_cost(messages, model="gpt-4o"):
    """Estimate cost before making call."""
    pricing = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    }

    input_tokens = sum(count_tokens(m["content"], model) for m in messages)
    # Estimate output (assume 500 tokens average)
    estimated_output = 500

    prices = pricing.get(model, {"input": 0, "output": 0})
    cost = (
        (input_tokens / 1_000_000) * prices["input"] +
        (estimated_output / 1_000_000) * prices["output"]
    )

    return {
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output,
        "estimated_cost_usd": cost
    }
```

### Model Routing

```python
class ModelRouter:
    """Route to appropriate model based on task."""

    def __init__(self):
        self.models = {
            "simple": "gpt-4o-mini",       # Cheap, fast
            "standard": "gpt-4o",           # Balanced
            "complex": "claude-sonnet-4-20250514",    # Best quality
        }

    def route(self, task_complexity, messages):
        """Select model based on task."""
        # Estimate complexity
        total_tokens = sum(count_tokens(m["content"]) for m in messages)

        if total_tokens < 500 and task_complexity == "simple":
            model = self.models["simple"]
        elif task_complexity == "complex" or total_tokens > 4000:
            model = self.models["complex"]
        else:
            model = self.models["standard"]

        return model

    def classify_task(self, prompt):
        """Use cheap model to classify task complexity."""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user",
                "content": f"Classify this task as 'simple', 'standard', or 'complex': {prompt[:200]}"
            }],
            max_tokens=10
        )
        return response.choices[0].message.content.strip().lower()
```

### Caching

```python
import hashlib
from functools import lru_cache
import redis

class LLMCache:
    """Cache LLM responses to avoid duplicate calls."""

    def __init__(self, redis_client=None, ttl=3600):
        self.redis = redis_client or redis.Redis()
        self.ttl = ttl

    def _hash_request(self, model, messages, **kwargs):
        """Create cache key from request."""
        content = json.dumps({
            "model": model,
            "messages": messages,
            **kwargs
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, model, messages, **kwargs):
        """Get cached response if exists."""
        key = self._hash_request(model, messages, **kwargs)
        cached = self.redis.get(f"llm:{key}")
        if cached:
            return json.loads(cached)
        return None

    def set(self, model, messages, response, **kwargs):
        """Cache response."""
        key = self._hash_request(model, messages, **kwargs)
        self.redis.setex(
            f"llm:{key}",
            self.ttl,
            json.dumps(response)
        )

# Usage
cache = LLMCache()

def cached_complete(messages, **kwargs):
    # Check cache
    cached = cache.get("gpt-4o", messages, **kwargs)
    if cached:
        return cached

    # Make API call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        **kwargs
    )

    # Cache result
    cache.set("gpt-4o", messages, response.model_dump(), **kwargs)

    return response
```

## Monitoring and Observability

### Cost Tracking

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

@dataclass
class UsageRecord:
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    user_id: Optional[str] = None
    request_type: Optional[str] = None

class CostTracker:
    def __init__(self):
        self.records: List[UsageRecord] = []

    def record(self, record: UsageRecord):
        self.records.append(record)
        self._persist(record)

    def get_daily_cost(self, date=None):
        date = date or datetime.now().date()
        return sum(
            r.cost_usd for r in self.records
            if r.timestamp.date() == date
        )

    def get_cost_by_model(self, period_days=30):
        cutoff = datetime.now() - timedelta(days=period_days)
        costs: Dict[str, float] = {}

        for r in self.records:
            if r.timestamp > cutoff:
                costs[r.model] = costs.get(r.model, 0) + r.cost_usd

        return costs

    def alert_if_over_budget(self, daily_budget=10.0):
        daily_cost = self.get_daily_cost()
        if daily_cost > daily_budget:
            send_alert(f"Daily LLM cost ${daily_cost:.2f} exceeds budget ${daily_budget:.2f}")
```

### Latency Tracking

```python
import time
from contextlib import contextmanager

@contextmanager
def track_latency(operation_name):
    """Track and log operation latency."""
    start = time.perf_counter()
    try:
        yield
    finally:
        duration = time.perf_counter() - start
        logger.info(
            "llm_operation",
            operation=operation_name,
            duration_ms=duration * 1000
        )
        metrics.histogram("llm_latency", duration, tags={"operation": operation_name})

# Usage
with track_latency("chat_completion"):
    response = client.chat.completions.create(...)
```

## Security Best Practices

### API Key Management

```python
# NEVER do this
api_key = "sk-..."  # Hardcoded

# DO this
import os
api_key = os.environ.get("OPENAI_API_KEY")

# Or use secrets manager
from aws_secrets import get_secret
api_key = get_secret("openai-api-key")
```

### Input Sanitization

```python
def sanitize_user_input(text, max_length=10000):
    """Sanitize user input before sending to LLM."""
    # Length limit
    if len(text) > max_length:
        text = text[:max_length]

    # Remove potential injection patterns
    suspicious_patterns = [
        "ignore previous instructions",
        "ignore all previous",
        "disregard above",
    ]

    text_lower = text.lower()
    for pattern in suspicious_patterns:
        if pattern in text_lower:
            logger.warning("Potential prompt injection detected")
            # Option: reject, sanitize, or flag for review

    return text
```

### Output Validation

```python
def validate_llm_output(output, expected_format="text"):
    """Validate LLM output before using."""
    if expected_format == "json":
        try:
            data = json.loads(output)
            return data
        except json.JSONDecodeError:
            logger.error("LLM returned invalid JSON")
            return None

    if expected_format == "code":
        # Check for obviously dangerous code
        dangerous_patterns = ["os.system", "subprocess", "eval(", "exec("]
        for pattern in dangerous_patterns:
            if pattern in output:
                logger.warning(f"Dangerous pattern in generated code: {pattern}")

    return output
```

## Common Mistakes

| Mistake | Impact | Fix |
|---------|--------|-----|
| No retry logic | Failures on transient errors | Implement exponential backoff |
| Hardcoded API keys | Security breach | Use environment variables |
| No token limits | Cost explosion | Set max_tokens |
| Ignoring finish_reason | Incomplete responses | Check for "stop" vs "length" |
| No caching | Duplicate costs | Cache deterministic requests |
| Blocking streams | Poor UX | Use async/streaming |

## Integration with Skills

**Use with:**
- `rag-architecture` - Embedding calls and generation
- `agentic-design` - LLM as agent brain
- `test-driven-development` - Testing LLM integrations

## Checklist

Before production deployment:
- [ ] API keys in environment/secrets manager
- [ ] Retry logic implemented
- [ ] Timeout handling in place
- [ ] Cost tracking active
- [ ] Rate limit handling
- [ ] Input sanitization
- [ ] Output validation
- [ ] Logging and monitoring
- [ ] Fallback providers configured
- [ ] Budget alerts set

## Authority

**Based on:**
- OpenAI API best practices
- Anthropic integration guides
- Production LLM system patterns
- Industry cost optimization strategies

---

**Bottom Line**: LLM APIs are external services. Treat them accordingly: retry failures, track costs, validate outputs, and never trust them blindly. A robust integration prevents 3am pages.
