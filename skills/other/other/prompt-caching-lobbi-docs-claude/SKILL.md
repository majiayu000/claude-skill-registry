---
name: prompt-caching
description: Prompt caching for Claude API to reduce latency by up to 85% and costs by up to 90%. Activate for cache_control, ephemeral caching, cache breakpoints, and performance optimization.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
triggers:
  - cache
  - prompt-caching
  - cache_control
  - ephemeral
  - cache breakpoint
  - latency
  - performance
  - cost optimization
dependencies:
  - llm-integration
related-skills:
  - extended-thinking
  - batch-processing
---

# Prompt Caching Skill

Leverage Anthropic's prompt caching to dramatically reduce latency and costs for repeated prompts.

## When to Use This Skill

- RAG systems with large static documents
- Multi-turn conversations with long instructions
- Code analysis with large codebase context
- Batch processing with shared prefixes
- Document analysis and summarization

## Core Concepts

### Cache Control Placement

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are a helpful assistant with access to a large knowledge base...",
            "cache_control": {"type": "ephemeral"}  # Cache this content
        }
    ],
    messages=[{"role": "user", "content": "What is...?"}]
)
```

### Cache Hierarchy

Cache breakpoints are checked in this order:
1. **Tools** - Tool definitions cached first
2. **System** - System prompts cached second
3. **Messages** - Conversation history cached last

### TTL Options

| TTL | Write Cost | Read Cost | Use Case |
|-----|-----------|-----------|----------|
| 5 minutes (default) | 1.25x base | 0.1x base | Interactive sessions |
| 1 hour | 2.0x base | 0.1x base | Batch processing, stable docs |

### Cache Requirements

- **Minimum tokens:** 1024-4096 (varies by model)
- **Maximum breakpoints:** 4 per request
- **Supported models:** Claude Opus 4.5, Sonnet 4.5, Haiku 4.5

## Implementation Patterns

### Pattern 1: Single Breakpoint (Recommended)

```python
# Best for: Document analysis, Q&A with static context
system = [
    {
        "type": "text",
        "text": large_document_content,
        "cache_control": {"type": "ephemeral"}  # Single breakpoint at end
    }
]
```

### Pattern 2: Multi-Turn Conversation

```python
# Cache grows with conversation
messages = [
    {"role": "user", "content": "First question"},
    {"role": "assistant", "content": "First answer"},
    {
        "role": "user",
        "content": "Follow-up question",
        "cache_control": {"type": "ephemeral"}  # Cache entire conversation
    }
]
```

### Pattern 3: RAG with Multiple Breakpoints

```python
system = [
    {
        "type": "text",
        "text": "Tool definitions and instructions",
        "cache_control": {"type": "ephemeral"}  # Breakpoint 1: Tools
    },
    {
        "type": "text",
        "text": retrieved_documents,
        "cache_control": {"type": "ephemeral"}  # Breakpoint 2: Documents
    }
]
```

### Pattern 4: Batch Processing with 1-Hour TTL

```python
# Warm the cache before batch
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=100,
    system=[{
        "type": "text",
        "text": shared_context,
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    }],
    messages=[{"role": "user", "content": "Initialize cache"}]
)

# Now run batch - all requests hit the cache
for item in batch_items:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": shared_context,
            "cache_control": {"type": "ephemeral", "ttl": "1h"}
        }],
        messages=[{"role": "user", "content": item}]
    )
```

## Performance Monitoring

### Check Cache Usage

```python
response = client.messages.create(...)

# Monitor these fields
cache_write = response.usage.cache_creation_input_tokens  # New cache written
cache_read = response.usage.cache_read_input_tokens       # Cache hit!
uncached = response.usage.input_tokens                    # After breakpoint

print(f"Cache hit rate: {cache_read / (cache_read + cache_write + uncached) * 100:.1f}%")
```

### Cost Calculation

```python
def calculate_cost(usage, model="claude-sonnet-4-20250514"):
    # Example rates (check current pricing)
    base_input_rate = 0.003  # per 1K tokens

    write_cost = (usage.cache_creation_input_tokens / 1000) * base_input_rate * 1.25
    read_cost = (usage.cache_read_input_tokens / 1000) * base_input_rate * 0.1
    uncached_cost = (usage.input_tokens / 1000) * base_input_rate

    return write_cost + read_cost + uncached_cost
```

## Cache Invalidation

Changes that invalidate cache:

| Change | Impact |
|--------|--------|
| Tool definitions | Entire cache invalidated |
| System prompt | System + messages invalidated |
| Any content before breakpoint | That breakpoint + later invalidated |

## Best Practices

### DO:
- Place breakpoint at END of static content
- Keep tools/instructions stable across requests
- Use 1-hour TTL for batch processing
- Monitor cache_read_input_tokens for savings

### DON'T:
- Place breakpoint in middle of dynamic content
- Change tool definitions frequently
- Expect cache to work with <1024 tokens
- Ignore the 20-block lookback limit

## Integration with Extended Thinking

```python
# Cache + Extended Thinking
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={"type": "enabled", "budget_tokens": 10000},
    system=[{
        "type": "text",
        "text": large_context,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "Analyze this..."}]
)
```

## See Also

- [[llm-integration]] - Claude API basics
- [[extended-thinking]] - Deep reasoning
- [[batch-processing]] - Bulk processing
