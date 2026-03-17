---
name: building-with-agent-memory
description: Build persistent memory systems for AI agents using Mem0, claude-mem, or custom implementations. Use when adding conversation memory, user preferences, or contextual recall to agents. Covers memory architecture patterns, retrieval strategies, and privacy controls. NOT for RAG systems (use building-rag-systems).
---

# Building Agent Memory Systems

Production-grade memory layers for AI agents that persist context across sessions.

## Quick Decision

| Need | Tool | Why |
|------|------|-----|
| Simple memory for any agent | Mem0 | Open-source, Python SDK, minimal setup |
| Claude Code agent memory | claude-mem | Automatic hooks, 3-layer retrieval |
| Enterprise/self-editing memory | Letta (MemGPT) | Agent-driven memory management |
| Custom memory | RAG + state management | Full control |

---

## Mem0: Primary Implementation

### Installation

```bash
pip install mem0ai
export OPENAI_API_KEY="your-key"
```

### Basic Usage

```python
from mem0 import Memory

m = Memory()

# Add memory from conversation
messages = [
    {"role": "user", "content": "Hi, I'm Alex. I love basketball and gaming."},
    {"role": "assistant", "content": "Hey Alex! I'll remember your interests."}
]
m.add(messages, user_id="alex")

# Search memories
results = m.search("What do you know about me?", filters={"user_id": "alex"})
# Returns: {"results": [{"memory": "Name is Alex. Enjoys basketball and gaming.", "score": 0.89}]}
```

### Default Configuration (OSS)

- **LLM**: OpenAI gpt-4.1-nano-2025-04-14 (fact extraction)
- **Embeddings**: text-embedding-3-small (1536 dims)
- **Vector Store**: Qdrant (on-disk at /tmp/qdrant)
- **History**: SQLite at ~/.mem0/history.db

### Memory Categories

| Category | Scope | Use Case |
|----------|-------|----------|
| `user_id` | Individual users | Preferences, identity, history |
| `agent_id` | Specific agents | Agent-specific context |
| `session_id` | Conversation | Temporary, conversation-scoped |
| `run_id` | Single execution | Within-session partitioning |

### Core Operations

```python
# Add with metadata
m.add(
    messages,
    user_id="alex",
    metadata={"category": "preferences", "project": "task-api"}
)

# Search with filters
results = m.search(
    "task preferences",
    filters={
        "user_id": "alex",
        "category": "preferences"
    }
)

# Search with date filter
results = m.search(
    query="recent interactions",
    filters={
        "AND": [
            {"user_id": "alex"},
            {"created_at": {"gte": "2024-07-01"}}
        ]
    }
)

# Update memory
m.update(memory_id="mem_123abc", new_content="Updated preference")

# Delete memory
m.delete(memory_id="mem_123abc")
```

### Custom Configuration

```python
from mem0 import Memory

config = {
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-3-5-sonnet-20241022",
            "api_key": "your-anthropic-key"
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "path": "./my_memories"  # Custom path
        }
    }
}

m = Memory.from_config(config)
```

---

## Memory Architecture Patterns

### Five Memory Types

```
┌────────────────────────────────────────────────────┐
│                   AGENT MEMORY                      │
├─────────────┬──────────────┬───────────────────────┤
│ Conversation│   Working    │     Long-term         │
│   Memory    │   Memory     │      Memory           │
│             │              │                       │
│ Last N      │ Current task │ ┌─────────────────┐   │
│ messages    │ context      │ │ Episodic Memory │   │
│             │              │ │ (events)        │   │
│ Volatile    │ Task-scoped  │ ├─────────────────┤   │
│             │              │ │ Semantic Memory │   │
│             │              │ │ (facts)         │   │
│             │              │ └─────────────────┘   │
└─────────────┴──────────────┴───────────────────────┘
```

| Type | Persistence | Scope | Example |
|------|-------------|-------|---------|
| **Conversation** | Session | Current chat | Last 10 messages |
| **Working** | Task | Current task | Active goal, intermediate results |
| **Episodic** | Long-term | Time-stamped events | "Last Tuesday you asked about X" |
| **Semantic** | Long-term | Facts/entities | "Alex works at Acme" |
| **Procedural** | Long-term | Learned patterns | How user structures tasks |

### Letta/MemGPT Two-Tier Architecture

```
┌─────────────────────────────────────────────────────┐
│              IN-CONTEXT (Core Memory)               │
│  ┌──────────────┐  ┌──────────────────────────┐    │
│  │ Persona Block│  │ Human Block              │    │
│  │ (agent)      │  │ (user info)              │    │
│  └──────────────┘  └──────────────────────────┘    │
│              Always visible to LLM                  │
└─────────────────────────────────────────────────────┘
                         │
                         │ (tool calls)
                         ▼
┌─────────────────────────────────────────────────────┐
│            OUT-OF-CONTEXT (External Memory)         │
│  ┌──────────────────┐  ┌────────────────────────┐  │
│  │ Archival Memory  │  │ Conversation History   │  │
│  │ (vector DB)      │  │ (full message log)     │  │
│  └──────────────────┘  └────────────────────────┘  │
│              Retrieved on-demand via tools          │
└─────────────────────────────────────────────────────┘
```

**Self-Editing Tools** (Letta pattern):
- `memory_replace(block, old_text, new_text)` - Targeted updates
- `memory_insert(block, text)` - Add new information
- `memory_rethink(block, new_content)` - Complete rewrite

---

## Retrieval Strategies

### Recency-Based

```python
def get_recent_memories(user_id: str, limit: int = 5):
    """Most recent memories first."""
    return m.search(
        query="",  # Empty query = recency sort
        filters={"user_id": user_id},
        top_k=limit
    )
```

### Relevance-Based (Semantic)

```python
def get_relevant_memories(user_id: str, query: str, limit: int = 5):
    """Semantic search over memories."""
    return m.search(
        query=query,
        filters={"user_id": user_id},
        top_k=limit,
        threshold=0.7  # Minimum similarity
    )
```

### Entity-Based

```python
def get_entity_memories(user_id: str, entity: str):
    """Memories mentioning specific entity."""
    return m.search(
        query=entity,
        filters={
            "user_id": user_id,
            "categories": {"contains": "entities"}
        }
    )
```

### Hybrid Retrieval

```python
def hybrid_retrieve(user_id: str, query: str, limit: int = 10):
    """Combine recency + relevance + entity."""
    # Get relevant
    relevant = m.search(query, filters={"user_id": user_id}, top_k=limit)

    # Extract entities from query
    entities = extract_entities(query)
    entity_memories = []
    for entity in entities:
        entity_memories.extend(
            m.search(entity, filters={"user_id": user_id}, top_k=3)
        )

    # Deduplicate and score
    all_memories = deduplicate(relevant + entity_memories)

    # Weight: 0.5*relevance + 0.3*recency + 0.2*entity_match
    return sorted(all_memories, key=weighted_score, reverse=True)[:limit]
```

---

## Context Window Management

### Memory Injection Pattern

```python
def build_prompt_with_memory(user_query: str, user_id: str) -> str:
    """Inject relevant memories before user query."""
    memories = m.search(user_query, filters={"user_id": user_id}, top_k=5)

    memory_context = "\n".join([
        f"- {mem['memory']}" for mem in memories['results']
    ])

    return f"""You know the following about this user:
{memory_context}

User query: {user_query}
"""
```

### Token Budget Management

```python
def fit_memories_to_budget(memories: list, budget_tokens: int = 2000) -> list:
    """Select memories that fit within token budget."""
    selected = []
    current_tokens = 0

    for mem in memories:
        mem_tokens = estimate_tokens(mem['memory'])
        if current_tokens + mem_tokens <= budget_tokens:
            selected.append(mem)
            current_tokens += mem_tokens
        else:
            break

    return selected
```

### Hierarchical Summarization

```python
def summarize_old_memories(user_id: str, older_than_days: int = 30):
    """Compress old memories into summaries."""
    old_memories = m.search(
        query="",
        filters={
            "user_id": user_id,
            "created_at": {"lte": f"{days_ago(older_than_days)}"}
        }
    )

    # Group by topic/category
    grouped = group_by_category(old_memories)

    # Generate summary per group
    for category, memories in grouped.items():
        summary = llm.summarize(memories)
        m.add(
            [{"role": "system", "content": f"Summary of {category}: {summary}"}],
            user_id=user_id,
            metadata={"type": "summary", "category": category}
        )

        # Delete original detailed memories
        for mem in memories:
            m.delete(mem['id'])
```

---

## FastAPI Integration Pattern

```python
from fastapi import FastAPI, Depends
from mem0 import Memory

app = FastAPI()
memory = Memory()

@app.post("/tasks")
async def create_task_with_memory(task: TaskCreate, user_id: str):
    # 1. Retrieve relevant memories
    preference_memories = memory.search(
        f"task preferences for {task.category}",
        filters={"user_id": user_id, "category": "preferences"}
    )

    pattern_memories = memory.search(
        f"past tasks like {task.title}",
        filters={"user_id": user_id, "category": "patterns"}
    )

    # 2. Apply memories to task creation
    task = enhance_task_with_preferences(task, preference_memories)
    task = estimate_time_from_patterns(task, pattern_memories)

    # 3. Create the task
    created_task = await create_task(task)

    # 4. Store this interaction as new memory
    memory.add([
        {"role": "user", "content": f"Created task: {task.title} in {task.category}"},
        {"role": "assistant", "content": f"Task created with estimated time: {task.estimated_hours}h"}
    ], user_id=user_id, metadata={"category": "interactions"})

    return created_task
```

---

## claude-mem: Claude Code Memory

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                   claude-mem                         │
├─────────────────────────────────────────────────────┤
│  5 Lifecycle Hooks:                                  │
│  • SessionStart    • PostToolUse   • SessionEnd     │
│  • UserPromptSubmit • Stop                          │
├─────────────────────────────────────────────────────┤
│  Worker Service: HTTP API on port 37777              │
│  Web Viewer: http://localhost:37777                  │
├─────────────────────────────────────────────────────┤
│  Storage:                                            │
│  • SQLite: Sessions, observations, summaries        │
│  • Chroma: Hybrid semantic + keyword search         │
└─────────────────────────────────────────────────────┘
```

### 3-Layer Token-Efficient Retrieval

```
Layer 1: search(query, type, limit)
→ Compact index (~50-100 tokens/result)
→ Returns observation IDs for filtering

Layer 2: timeline(observation_id, context_window)
→ Chronological context around observations
→ Understand sequence of events

Layer 3: get_observations(ids)
→ Full details only for filtered IDs
→ ~500-1,000 tokens/result

Result: 10x token savings by filtering before fetching
```

### Privacy Controls

```markdown
<private>
API_KEY=secret123
Sensitive project data here
</private>

Everything inside <private> tags is excluded from memory.
```

---

## Memory Prioritization

### Relevance Scoring Formula

```python
def calculate_relevance_score(memory, query, current_time):
    """
    Score = 0.5 * semantic_similarity
          + 0.3 * recency_decay
          + 0.2 * access_frequency
    """
    semantic = cosine_similarity(embed(memory.text), embed(query))

    days_old = (current_time - memory.created_at).days
    recency = math.exp(-days_old / 30)  # Decay over 30 days

    frequency = memory.access_count / max_access_count

    return 0.5 * semantic + 0.3 * recency + 0.2 * frequency
```

### Contradiction Resolution

```python
def handle_contradiction(old_memory, new_memory):
    """Newer information wins for preferences."""
    if new_memory.created_at > old_memory.created_at:
        # Update old memory with new information
        m.update(old_memory.id, new_memory.content)
        return "updated"
    return "kept_old"
```

---

## Safety & Privacy

### NEVER Store
- Passwords, API keys, tokens
- SSN, credit card numbers
- Medical records without explicit consent
- Information user explicitly asks to forget

### ALWAYS Implement
- User consent before memory creation
- Clear disclosure of what's stored
- Easy opt-out mechanisms (delete all)
- GDPR/CCPA compliance for deletion requests
- Encryption at rest for memory stores
- Access controls for multi-tenant systems

### Right to Forget

```python
async def forget_user(user_id: str):
    """GDPR-compliant deletion."""
    # Get all user memories
    all_memories = m.search("", filters={"user_id": user_id}, top_k=10000)

    # Delete each one
    for mem in all_memories['results']:
        m.delete(mem['id'])

    # Audit log
    log.info(f"Deleted all memories for user {user_id}")
```

---

## Anti-Patterns

| Don't | Do Instead |
|-------|------------|
| Store everything | Prioritize by relevance |
| Infinite memory growth | Regular consolidation cycles |
| No user consent | Explicit opt-in for memory |
| Store PII freely | Anonymize or exclude sensitive data |
| Ignore contradictions | Timestamp-based resolution |
| Skip privacy controls | Implement `<private>` patterns |
| Full retrieval every time | Token-budget constrained retrieval |

---

## References

- [Mem0 Documentation](https://docs.mem0.ai/)
- [Mem0 GitHub](https://github.com/mem0ai/mem0)
- [claude-mem GitHub](https://github.com/thedotmack/claude-mem)
- [MemGPT Paper](https://arxiv.org/abs/2310.08560)
- [Letta Documentation](https://docs.letta.com/)
