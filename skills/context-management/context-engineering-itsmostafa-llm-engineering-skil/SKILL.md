---
name: context-engineering
description: Strategies for managing LLM context windows effectively in AI agents. Use when building agents that handle long conversations, multi-step tasks, tool orchestration, or need to maintain coherence across extended interactions.
---

# Context Engineering

Context engineering is the discipline of curating and maintaining the optimal set of tokens during LLM inference. Unlike prompt engineering (crafting individual prompts), context engineering focuses on what information enters the context window and when.

## Table of Contents

- [Core Principles](#core-principles)
- [Context Management Strategies](#context-management-strategies)
- [System Prompt Design](#system-prompt-design)
- [Tool Design for Context Efficiency](#tool-design-for-context-efficiency)
- [Long-Horizon Task Patterns](#long-horizon-task-patterns)
- [Implementation Patterns](#implementation-patterns)
- [Best Practices](#best-practices)
- [References](#references)

## Core Principles

### Context as a Finite Resource

LLMs have limited "attention budgets." As context length increases, models experience **context rot**—decreased ability to accurately recall information. The goal is finding the smallest possible set of high-signal tokens that maximize desired outcomes.

```
Effective Context = Relevant Information / Total Tokens
```

**Key insight**: More context isn't better. The right context is better.

### The Context Pollution Problem

Every token added to context has costs:
- Increased latency and compute
- Diluted attention to important information
- Higher risk of hallucination from conflicting data
- Reduced model performance on retrieval tasks

## Context Management Strategies

### 1. Context Trimming

Drop older conversation turns, keeping only the last N turns.

| Aspect | Details |
|--------|---------|
| **Mechanism** | Sliding window over conversation history |
| **Pros** | Deterministic, zero latency, preserves recent context verbatim |
| **Cons** | Abrupt loss of long-range context, "amnesia" effect |
| **Best for** | Independent tasks, short interactions, predictable workflows |

```python
def trim_context(messages: list, keep_last_n: int = 10) -> list:
    """Keep system message + last N turns."""
    system_msgs = [m for m in messages if m["role"] == "system"]
    other_msgs = [m for m in messages if m["role"] != "system"]
    return system_msgs + other_msgs[-keep_last_n:]
```

### 2. Context Summarization

Compress prior messages into structured summaries.

| Aspect | Details |
|--------|---------|
| **Mechanism** | LLM generates summary of older context |
| **Pros** | Retains long-range memory, smoother UX, scalable |
| **Cons** | Summarization bias risk, added latency, potential compounding errors |
| **Best for** | Complex multi-step tasks, long-horizon interactions |

```python
SUMMARIZATION_PROMPT = """Summarize the conversation so far, preserving:
1. Key decisions made
2. Important context established
3. Current task state and goals
4. Any constraints or preferences expressed

Be concise but complete. Output as structured markdown."""

async def summarize_context(messages: list, model) -> str:
    """Generate a summary of conversation history."""
    conversation_text = format_messages_for_summary(messages)
    response = await model.generate(
        system=SUMMARIZATION_PROMPT,
        user=conversation_text
    )
    return response.content
```

### 3. Hybrid Approach

Combine trimming and summarization for optimal balance.

```python
class HybridContextManager:
    def __init__(
        self,
        keep_recent: int = 5,      # Recent turns to keep verbatim
        summary_threshold: int = 20, # When to trigger summarization
    ):
        self.keep_recent = keep_recent
        self.summary_threshold = summary_threshold
        self.running_summary = ""

    def process(self, messages: list) -> list:
        if len(messages) < self.summary_threshold:
            return messages

        # Summarize older messages
        old_messages = messages[:-self.keep_recent]
        self.running_summary = summarize(old_messages, self.running_summary)

        # Return summary + recent messages
        return [
            {"role": "system", "content": f"Previous context:\n{self.running_summary}"},
            *messages[-self.keep_recent:]
        ]
```

## System Prompt Design

### Principles for Context-Efficient Prompts

1. **Clear and direct language**: Avoid ambiguity that requires clarification turns
2. **Structured sections**: Organize by purpose (role, capabilities, constraints)
3. **Minimal yet comprehensive**: Include only what affects behavior
4. **Self-contained instructions**: Reduce need for context retrieval

### Example Structure

```markdown
# Role
You are [specific role] that [primary function].

# Capabilities
- [Capability 1 with scope]
- [Capability 2 with scope]

# Constraints
- [Hard constraint]
- [Preference]

# Output Format
[Specific format requirements]
```

## Tool Design for Context Efficiency

### Just-in-Time Context Loading

Instead of front-loading all possible context, load information dynamically as needed.

```python
# Anti-pattern: Loading everything upfront
context = load_all_user_data()  # Large, mostly unused
context += load_all_documents()  # Even larger

# Better: Just-in-time retrieval
tools = [
    Tool(
        name="get_user_preference",
        description="Get specific user preference by key",
        # Only fetches what's needed when asked
    ),
    Tool(
        name="search_documents",
        description="Search documents by query",
        # Returns relevant subset
    ),
]
```

### Tool Design Principles

1. **Self-contained**: Each tool returns complete, usable information
2. **Scoped**: Tools do one thing well
3. **Descriptive**: Names and descriptions guide LLM toward correct usage
4. **Error-robust**: Return informative errors that don't pollute context

```python
# Well-designed tool
def search_codebase(query: str, max_results: int = 5) -> str:
    """Search codebase for relevant code snippets.

    Args:
        query: Natural language description of what to find
        max_results: Maximum snippets to return (default 5)

    Returns:
        Formatted code snippets with file paths and line numbers,
        or 'No results found' if nothing matches.
    """
    results = perform_search(query, limit=max_results)
    if not results:
        return "No results found for query."
    return format_results(results)  # Concise, structured output
```

## Long-Horizon Task Patterns

### Pattern 1: Compaction

Periodically compress conversation history to reclaim context space.

```python
async def compaction_loop(agent, messages, task):
    while not task.complete:
        # Process next step
        response = await agent.run(messages)
        messages.append(response)

        # Compact when approaching limit
        if estimate_tokens(messages) > TOKEN_LIMIT * 0.8:
            summary = await summarize_context(messages[:-3])
            messages = [
                {"role": "system", "content": agent.system_prompt},
                {"role": "assistant", "content": f"Summary of progress:\n{summary}"},
                *messages[-3:]  # Keep recent context
            ]

    return messages
```

### Pattern 2: Structured Note-Taking

Agent maintains external notes, retrieving as needed.

```python
class NoteTakingAgent:
    def __init__(self):
        self.notes = {}  # Key-value store outside context

    async def run(self, messages):
        tools = [
            Tool("save_note", self.save_note, "Save information for later"),
            Tool("get_note", self.get_note, "Retrieve saved information"),
            Tool("list_notes", self.list_notes, "List all saved note keys"),
        ]
        return await self.agent.run(messages, tools=tools)

    def save_note(self, key: str, content: str) -> str:
        self.notes[key] = content
        return f"Saved note: {key}"

    def get_note(self, key: str) -> str:
        return self.notes.get(key, f"No note found for key: {key}")
```

### Pattern 3: Sub-Agent Architecture

Delegate focused tasks to specialized agents with clean context.

```python
class OrchestratorAgent:
    def __init__(self):
        self.sub_agents = {
            "researcher": ResearchAgent(),
            "coder": CodingAgent(),
            "reviewer": ReviewAgent(),
        }

    async def delegate(self, task: str, agent_type: str) -> str:
        """Delegate to sub-agent, receive condensed summary."""
        agent = self.sub_agents[agent_type]

        # Sub-agent works with fresh context
        result = await agent.run(task)

        # Return only essential findings to main context
        return result.summary  # Not the full conversation
```

**Benefits**:
- Each sub-agent has focused, clean context
- Main agent receives condensed results
- Parallelization opportunities
- Failure isolation

## Implementation Patterns

### Session Memory Manager

```python
class SessionMemory:
    def __init__(
        self,
        keep_last_n_turns: int = 5,
        context_limit: int = 100_000,  # tokens
        summarizer = None,
    ):
        self.keep_last_n_turns = keep_last_n_turns
        self.context_limit = context_limit
        self.summarizer = summarizer
        self.messages = []
        self.summary = ""

    async def add_message(self, message: dict):
        self.messages.append(message)
        await self._maybe_compact()

    async def _maybe_compact(self):
        current_tokens = estimate_tokens(self.messages)

        if current_tokens > self.context_limit * 0.8:
            # Summarize all but recent messages
            old_messages = self.messages[:-self.keep_last_n_turns]
            new_summary = await self.summarizer.summarize(
                old_messages,
                previous_summary=self.summary
            )
            self.summary = new_summary
            self.messages = self.messages[-self.keep_last_n_turns:]

    def get_context(self) -> list:
        context = []
        if self.summary:
            context.append({
                "role": "system",
                "content": f"Conversation summary:\n{self.summary}"
            })
        context.extend(self.messages)
        return context
```

### Token Estimation

```python
def estimate_tokens(messages: list) -> int:
    """Rough token estimation (4 chars ≈ 1 token for English)."""
    total_chars = sum(
        len(m.get("content", ""))
        for m in messages
    )
    return total_chars // 4

def estimate_tokens_accurate(messages: list, model: str) -> int:
    """Accurate token count using tiktoken."""
    import tiktoken
    encoding = tiktoken.encoding_for_model(model)
    return sum(
        len(encoding.encode(m.get("content", "")))
        for m in messages
    )
```

## Best Practices

1. **Treat context as precious**: Every token has a cost. Include only information that improves task performance.

2. **Use progressive disclosure**: Start minimal, expand context only when needed via tools.

3. **Design for recoverability**: Agents should be able to reconstruct critical context from external sources.

4. **Monitor context health**: Track token usage, retrieval accuracy, and task completion rates.

5. **Prefer structured over raw data**: JSON, markdown tables, and clear formatting improve information density.

6. **Implement graceful degradation**: When context limits approach, prioritize recent and high-signal information.

7. **Test with long conversations**: Validate agent behavior after many turns, not just initial interactions.

8. **Separate concerns**: Use different context regions for system instructions, user history, and tool outputs.

9. **Version your summaries**: When compacting, maintain enough structure to debug summarization issues.

10. **Measure and iterate**: Context engineering is empirical—test what information actually improves outcomes.

## References

- [reference/evaluation-strategies.md](reference/evaluation-strategies.md) - Testing context management effectiveness
- [reference/summarization-patterns.md](reference/summarization-patterns.md) - Detailed summarization implementations
