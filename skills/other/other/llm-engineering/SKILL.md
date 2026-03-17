---
name: llm-engineering
description: Patterns for building LLM applications - prompt engineering, RAG pipelines, cost optimization, multi-model routing, and evaluation. Auto-triggers when working with AI/LLM code.
---

# LLM Engineering Skill

## Prompt Engineering Patterns

### Structured Output

```python
# Force JSON output with schema
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": prompt}],
    system="Respond with valid JSON matching this schema: {\"name\": str, \"score\": float}",
)

# Anthropic tool_use for guaranteed structured output
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    tools=[{
        "name": "extract_data",
        "description": "Extract structured data",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "score": {"type": "number"},
            },
            "required": ["name", "score"],
        },
    }],
    tool_choice={"type": "tool", "name": "extract_data"},
    messages=[{"role": "user", "content": prompt}],
)
```

### Few-Shot Prompting

```python
EXAMPLES = """
Input: "The movie was terrible"
Output: {"sentiment": "negative", "confidence": 0.95}

Input: "I loved every minute of it"
Output: {"sentiment": "positive", "confidence": 0.98}

Input: "It was okay, nothing special"
Output: {"sentiment": "neutral", "confidence": 0.72}
"""

prompt = f"{EXAMPLES}\n\nInput: \"{user_text}\"\nOutput:"
```

### Chain of Thought

```python
# Explicit CoT prompting
system = """Think step by step:
1. Identify the key entities
2. Determine relationships between them
3. Formulate your answer based on the evidence
4. Rate your confidence (0-1)

Show your reasoning before the final answer."""
```

## Multi-Model Routing

### Cost-Performance Tiers

| Tier     | Model      | Cost/1M tokens       | Use Case                            |
| -------- | ---------- | -------------------- | ----------------------------------- |
| Fast     | Haiku 4.5  | $0.25 in / $1.25 out | Classification, extraction, routing |
| Balanced | Sonnet 4.5 | $3 in / $15 out      | Code generation, analysis, general  |
| Premium  | Opus 4.6   | $15 in / $75 out     | Complex reasoning, architecture     |

### Router Pattern

```python
def route_request(task: str, complexity: str) -> str:
    """Route to appropriate model based on task complexity."""
    routing = {
        "classify": "claude-haiku-4-5-20251001",
        "extract": "claude-haiku-4-5-20251001",
        "summarize": "claude-sonnet-4-5-20250929",
        "generate": "claude-sonnet-4-5-20250929",
        "architect": "claude-opus-4-6",
        "reason": "claude-opus-4-6",
    }
    if complexity == "simple":
        return "claude-haiku-4-5-20251001"
    return routing.get(task, "claude-sonnet-4-5-20250929")
```

### Fallback Chain

```python
import os

# Only include models you have API keys for
MODELS = [
    m for m in [
        "claude-sonnet-4-5-20250929" if os.getenv("ANTHROPIC_API_KEY") else None,
        "gpt-4o" if os.getenv("OPENAI_API_KEY") else None,
        "gemini-2.0-flash" if os.getenv("GEMINI_API_KEY") else None,
    ] if m
]

async def call_with_fallback(prompt: str) -> str:
    if not MODELS:
        raise ConfigError("No LLM API keys configured")
    for model in MODELS:
        try:
            return await call_model(model, prompt)
        except (RateLimitError, ServiceUnavailableError):
            continue
    raise AllModelsFailedError()
```

## RAG Pipeline Patterns

### Chunking Strategies

| Strategy  | Chunk Size        | Overlap           | Best For              |
| --------- | ----------------- | ----------------- | --------------------- |
| Fixed     | 512 tokens        | 50 tokens         | General documents     |
| Semantic  | Variable          | Sentence boundary | Technical docs        |
| Recursive | 1000 chars        | 200 chars         | Code, structured text |
| Document  | Full page/section | None              | Short documents       |

### Retrieval Pipeline

```python
async def rag_query(question: str, top_k: int = 5) -> str:
    # 1. Embed the query
    query_embedding = await embed(question)

    # 2. Retrieve relevant chunks
    chunks = await vector_store.similarity_search(
        query_embedding, top_k=top_k
    )

    # 3. Rerank (optional but improves quality)
    ranked = rerank(question, chunks, top_n=3)

    # 4. Build context
    context = "\n\n---\n\n".join(c.text for c in ranked)

    # 5. Generate answer with citations
    return await generate(
        system="Answer based on the provided context. Cite sources.",
        prompt=f"Context:\n{context}\n\nQuestion: {question}",
    )
```

### Embedding Best Practices

- Normalize embeddings for cosine similarity
- Use the same model for query and document embeddings
- Cache embeddings (they're deterministic)
- Batch embed operations (cheaper and faster)
- Store metadata alongside vectors for filtering

## Cost Optimization

### Token Counting

```python
import anthropic

# Count tokens before sending
client = anthropic.Anthropic()
token_count = client.count_tokens(prompt)

# Estimate cost
INPUT_COST_PER_M = 3.00  # Sonnet
OUTPUT_COST_PER_M = 15.00
estimated_cost = (token_count / 1_000_000) * INPUT_COST_PER_M
```

### Cost Reduction Strategies

| Strategy                              | Savings               | Tradeoff                 |
| ------------------------------------- | --------------------- | ------------------------ |
| Use Haiku for routing/classification  | 90%+                  | Slightly less capable    |
| Cache system prompts (prompt caching) | 90% on cached portion | 25% write premium        |
| Batch API for non-urgent work         | 50%                   | 24hr turnaround          |
| Shorter prompts (remove fluff)        | 10-30%                | Requires careful editing |
| Cache responses for identical inputs  | 100% on cache hit     | Stale responses possible |

### Prompt Caching (Anthropic)

```python
response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    system=[
        {
            "type": "text",
            "text": large_system_prompt,  # Cached after first call
            "cache_control": {"type": "ephemeral"},
        }
    ],
    messages=[{"role": "user", "content": user_query}],
)
```

## Evaluation

### Offline Evaluation

```python
def evaluate_pipeline(test_cases: list[dict]) -> dict:
    results = {"correct": 0, "total": len(test_cases)}
    for case in test_cases:
        output = pipeline(case["input"])
        if matches(output, case["expected"]):
            results["correct"] += 1
    results["accuracy"] = results["correct"] / results["total"]
    return results
```

### LLM-as-Judge

```python
JUDGE_PROMPT = """Rate the following response on a scale of 1-5:

Question: {question}
Response: {response}
Reference: {reference}

Criteria:
- Accuracy (does it match the reference?)
- Completeness (does it cover all key points?)
- Conciseness (is it free of unnecessary content?)

Return JSON: {"accuracy": int, "completeness": int, "conciseness": int}"""
```

### Key Metrics

| Metric             | Formula              | Good Target       |
| ------------------ | -------------------- | ----------------- |
| Accuracy           | correct / total      | >90%              |
| Latency (p50)      | median response time | <2s               |
| Latency (p99)      | 99th percentile      | <10s              |
| Cost per query     | tokens \* rate       | project-dependent |
| Hallucination rate | fabricated / total   | <5%               |

## Error Handling

```python
import anthropic

try:
    response = client.messages.create(...)
except anthropic.RateLimitError:
    # Back off and retry (use exponential backoff)
    await asyncio.sleep(backoff_seconds)
except anthropic.BadRequestError as e:
    # Input too long, invalid params
    logger.error("Bad request: %s", e)
    raise
except anthropic.APIConnectionError:
    # Network issue - retry or fallback
    return await call_with_fallback(prompt)
```

## Activation Triggers

This skill auto-activates when prompts contain:

- "llm", "language model", "prompt engineering"
- "rag", "retrieval", "embedding", "vector"
- "anthropic", "openai", "claude api", "gpt"
- "token", "cost optimization", "model routing"
- "few-shot", "chain of thought", "evaluation"

## Integration

- **@ai-engineer** agent: LLM application development
- **api-design** skill: API patterns for LLM services
- **async-patterns** skill: Concurrent LLM calls
