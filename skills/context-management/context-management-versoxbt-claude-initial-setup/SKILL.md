---
name: context-management
description: >
  Strategies for managing AI agent context windows including optimization, summarization,
  retrieval-augmented generation, progressive disclosure, and pruning. Use when the user
  is hitting context limits, building long-running agents, implementing RAG, optimizing
  token usage, or designing systems that need to manage large amounts of information
  within limited context windows.
---

# Context Management

Strategies for optimizing AI agent context windows. Covers summarization, RAG,
progressive disclosure, pruning, and token budgeting for long-running agents.

## When to Use
- User is hitting context window limits in agent workflows
- User is building long-running agents that accumulate context
- User needs retrieval-augmented generation (RAG) patterns
- User wants to optimize token usage and reduce costs
- User is designing memory systems for agents

## Core Patterns

### Sliding Window with Summarization

Keep recent messages in full while summarizing older ones.

```python
def manage_context(messages: list[dict], max_tokens: int = 50000) -> list[dict]:
    token_count = count_tokens(messages)

    if token_count <= max_tokens:
        return messages

    # Keep system message, summarize old messages, keep recent ones
    system_msg = messages[0] if messages[0]["role"] == "system" else None
    conversation = messages[1:] if system_msg else messages

    # Split: older half gets summarized, recent half stays intact
    midpoint = len(conversation) // 2
    older = conversation[:midpoint]
    recent = conversation[midpoint:]

    # Summarize older messages
    summary = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system="Summarize this conversation, preserving key decisions, facts, and action items.",
        messages=[{"role": "user", "content": json.dumps(older)}]
    )

    summary_msg = {
        "role": "user",
        "content": f"[Summary of earlier conversation]\n{summary.content[0].text}"
    }

    result = []
    if system_msg:
        result.append(system_msg)
    result.append(summary_msg)
    result.extend(recent)
    return result
```

### Retrieval-Augmented Generation (RAG)

Fetch relevant context on demand instead of loading everything upfront.

```python
from anthropic import Anthropic

client = Anthropic()

def rag_agent(question: str, knowledge_base) -> str:
    # Step 1: Generate search queries from the question
    query_response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=512,
        system="Generate 3 search queries to find relevant information. Return a JSON array of strings.",
        messages=[{"role": "user", "content": question}]
    )
    queries = json.loads(query_response.content[0].text)

    # Step 2: Retrieve relevant chunks
    chunks = []
    for query in queries:
        results = knowledge_base.search(query, top_k=3)
        chunks.extend(results)

    # Deduplicate and rank by relevance
    unique_chunks = deduplicate(chunks)
    top_chunks = sorted(unique_chunks, key=lambda c: c.score, reverse=True)[:5]

    # Step 3: Answer with retrieved context
    context = "\n\n---\n\n".join(
        f"Source: {c.metadata['source']}\n{c.text}" for c in top_chunks
    )

    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=4096,
        system="""Answer based on the provided context. If the context does not contain
enough information, say so. Cite sources using [Source: filename] format.""",
        messages=[{
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {question}"
        }]
    )
    return response.content[0].text
```

### Progressive Disclosure

Start with high-level summaries and drill down only when needed.

```python
def progressive_context(codebase_path: str, task: str) -> str:
    # Level 1: Project overview (minimal tokens)
    overview = generate_project_overview(codebase_path)

    response = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=2048,
        tools=drill_down_tools,
        system="You have a project overview. Use tools to read specific files when needed.",
        messages=[{
            "role": "user",
            "content": f"Project overview:\n{overview}\n\nTask: {task}"
        }]
    )

    # Claude will request specific files via tools rather than
    # loading the entire codebase into context upfront
    return run_tool_loop(response)

def generate_project_overview(path: str) -> str:
    """Generate a concise project map: file tree + key file summaries."""
    tree = get_file_tree(path, max_depth=3)
    key_files = ["README.md", "package.json", "src/index.ts"]
    summaries = {f: summarize_file(f) for f in key_files if os.path.exists(f)}
    return f"File tree:\n{tree}\n\nKey files:\n{json.dumps(summaries, indent=2)}"
```

### Context Pruning

Remove low-value content from context to make room for high-value information.

```python
def prune_context(messages: list[dict], budget_tokens: int) -> list[dict]:
    """Remove low-value messages while preserving coherence."""
    scored = []
    for i, msg in enumerate(messages):
        score = compute_relevance_score(msg, i, len(messages))
        scored.append((score, i, msg))

    # Sort by score descending, take messages within budget
    scored.sort(key=lambda x: x[0], reverse=True)

    kept = []
    used_tokens = 0
    for score, idx, msg in scored:
        msg_tokens = count_tokens_for_message(msg)
        if used_tokens + msg_tokens <= budget_tokens:
            kept.append((idx, msg))
            used_tokens += msg_tokens

    # Restore original order
    kept.sort(key=lambda x: x[0])
    return [msg for _, msg in kept]

def compute_relevance_score(msg: dict, position: int, total: int) -> float:
    """Score message relevance. Higher = more important to keep."""
    score = 0.0
    # Recent messages are more relevant
    recency = position / total
    score += recency * 0.4
    # System messages are always important
    if msg["role"] == "system":
        score += 1.0
    # Tool results with errors are important
    if "is_error" in str(msg.get("content", "")):
        score += 0.3
    # Long assistant responses often contain key analysis
    content_len = len(str(msg.get("content", "")))
    if msg["role"] == "assistant" and content_len > 500:
        score += 0.2
    return score
```

### Token Budgeting

Allocate token budgets across different context components.

```python
def allocate_token_budget(
    total_budget: int,
    system_prompt: str,
    tools: list,
    conversation: list
) -> dict:
    """Allocate tokens across context components."""
    system_tokens = count_tokens(system_prompt)
    tool_tokens = count_tokens(json.dumps(tools))
    reserved_output = 4096  # Reserve for response

    available = total_budget - system_tokens - tool_tokens - reserved_output

    # Allocate remaining budget
    return {
        "system": system_tokens,
        "tools": tool_tokens,
        "output_reserved": reserved_output,
        "conversation_budget": int(available * 0.6),   # 60% for conversation
        "retrieval_budget": int(available * 0.3),       # 30% for RAG context
        "scratch_budget": int(available * 0.1),         # 10% for working memory
        "total_available": available
    }
```

## Anti-Patterns
- Loading entire codebases into context instead of using progressive disclosure
- Not counting tokens before sending (leads to truncation or API errors)
- Summarizing with the same expensive model used for the main task (use Haiku)
- Keeping all tool call/result pairs in history (prune resolved tool interactions)
- Using a single giant system prompt instead of caching stable parts
- Not deduplicating RAG results (wastes tokens on repeated information)
- Ignoring prompt caching for repeated context (system prompts, tool definitions)

## Quick Reference

| Strategy | Token Savings | Tradeoff |
|----------|--------------|----------|
| Sliding window | 40-60% | Loses old details |
| Summarization | 50-80% | Lossy compression |
| RAG | 70-90% | Retrieval latency |
| Progressive disclosure | 60-80% | More API calls |
| Pruning | 20-40% | May lose relevant context |
| Prompt caching | 90% cost on hits | Ephemeral (5 min TTL) |

Context window sizes:
- Claude Sonnet/Opus: 200K tokens input
- Output: up to 64K tokens (with extended thinking)

Rule of thumb: Keep context under 80% of max to leave room for response quality.
