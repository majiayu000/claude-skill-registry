---
name: store-memory
version: "1.0.0"
description: >
  Store information in the hierarchical memory system. Supports three tiers:
  working (ephemeral), episodic (recent events), and semantic (permanent patterns).
  Use for learning from observations. Keywords: memory, store, learn, remember,
  episodic, semantic, pattern.
metadata:
  domain: general
  category: memory
  requires-approval: false
  confidence: 0.9
  mcp-servers: []
---

# Store Memory

## Preconditions

Before applying this skill, verify:

- Memory system is initialized (Qdrant available)
- Content to store is meaningful
- Appropriate tier is selected

## Actions

### 1. Classify Memory Tier

Determine which memory tier to use:
- **Working**: Temporary context, 1-hour TTL, max 20 items
- **Episodic**: Recent events, 7-30 day retention, time-decayed
- **Semantic**: Permanent patterns, never expires

### 2. Extract Structured Facts

Use LLM to extract key facts from content:
```yaml
input: $raw_content
max_length: 4000
temperature: 0.1
output: list[str]
```

### 3. Store in Memory Tier

**For Working Memory:**
```python
memory.add_working(
    content=content,
    metadata={"source": source, "timestamp": now}
)
```

**For Episodic Memory:**
```python
memory.add_episodic(
    content=content,
    user_id=user_id,
    metadata={"event_type": type, "timestamp": now}
)
```

**For Semantic Memory:**
```python
memory.add_semantic(
    content=content,
    user_id=user_id,
    metadata={"pattern_type": type, "confidence": confidence}
)
```

## Success Criteria

The skill succeeds when:

- [ ] Content successfully stored
- [ ] Memory retrievable via search
- [ ] Metadata properly indexed

## Failure Handling

If storage fails:

1. Check Qdrant connectivity
2. Verify content is not empty
3. Fall back to working memory if persistent storage unavailable

## Examples

**Input Context:**
```json
{
  "tier": "episodic",
  "content": "Pod nginx-abc123 crashed due to OOM. Increased memory limit from 512Mi to 1Gi.",
  "user_id": "k8s-monitor",
  "event_type": "remediation_success",
  "source": "remediator"
}
```

**Expected Output:**
```json
{
  "stored": true,
  "tier": "episodic",
  "memory_id": "mem_abc123",
  "facts_extracted": 2
}
```
