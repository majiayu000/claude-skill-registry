---
name: vector-memory
description: "Persistent vector memory for Claude Code via LanceDB. Use when: remembering across sessions, storing lessons, recalling past decisions, maintaining context continuity. Tools: memory_store, memory_recall, memory_update, memory_forget, memory_merge."
---

# Vector Memory

Long-term memory that persists across sessions. Store facts, decisions, lessons, preferences — recall them later via semantic search.

Vector memory is a **retrieval layer**, not a source of truth. Files and code are the source of truth; vector memory helps you find relevant context fast.

## References

- [tools-reference.md](references/tools-reference.md) — All MCP tools with full parameter docs
- [retrieval-internals.md](references/retrieval-internals.md) — Hybrid pipeline, Weibull decay model (load when debugging retrieval)

---

## When to Store

| Signal | Category | Example |
|--------|----------|---------|
| User states a preference | `preference` | "I prefer tabs over spaces" |
| A fact is established | `fact` | "The API uses OAuth 2.0 with PKCE" |
| A decision is made with rationale | `decision` | "Chose PostgreSQL over MongoDB because..." |
| A mistake was made and corrected | `lesson` | "CSS not applying → check for syntax errors above" |
| An important entity is introduced | `entity` | "Acme Corp is the client, contact: jane@acme.com" |
| A reusable technique is learned | `skill` | "Remotion animations use interpolate()" |

### When NOT to Store

- Temporary task state (use files)
- Things already in committed code or docs
- Conversation summaries ("today we discussed X") — store the **extracted knowledge**, not the summary
- Obvious facts the user can easily re-state

---

## Memory Hygiene

1. **Short and atomic** — Each memory < 500 chars, one concept per memory
2. **No conversation summaries** — Store distilled knowledge, not "we talked about X"
3. **Check before storing** — `memory_recall` first to avoid duplicates
4. **Accurate categories** — Category affects retrieval quality; pick the right one

---

## Mandatory Trigger Points

| When | Action |
|------|--------|
| **Session start** | `memory_recall` with keywords from user's first message |
| **After a decision** | `memory_store` with category `decision` |
| **After a mistake** | `memory_store` × 2 — dual-layer (see below) |
| **Tool fails / error occurs** | `memory_recall` first — you may have hit this before |
| **Session end** | Review: any new facts, decisions, or lessons worth persisting? |

### Recall Before Retry

When a tool fails or you encounter an error, **search memory before retrying**. You may have solved this exact problem before:

```
memory_recall(query: "npm install native module EPERM Windows")
```

This one habit prevents repeating the same mistakes across sessions.

---

## Dual-Layer Storage (Lessons)

Every mistake or lesson learned gets stored **twice**:

```
# Layer 1: Technical fact (what happened)
memory_store(
  text: "npm publish with noEmit: true ships no dist/ — bin entry fails in npx",
  category: "fact",
  importance: 0.8
)

# Layer 2: Actionable rule (what to do next time)
memory_store(
  text: "Always build to dist/ before npm publish, never rely on runtime transpilers for published packages",
  category: "lesson",
  importance: 0.9,
  lesson_trigger: "publishing npm packages with TypeScript",
  lesson_rule: "always build to dist/ before publish",
  lesson_principle: "published packages must be self-contained"
)
```

Why two? Different queries find different layers. "Why did publish fail?" hits the fact. "How should I publish TypeScript?" hits the lesson.

---

## Category Reference

| Meaning | Category | Importance | Typical use |
|---------|----------|------------|-------------|
| User preference | `preference` | 0.8 | "I prefer TypeScript" |
| Objective fact | `fact` | 0.7–0.8 | "The API uses LanceDB for vector storage" |
| Decision with rationale | `decision` | 0.85 | "Chose LanceDB because it's embedded, no server needed" |
| Entity info | `entity` | 0.7 | "DeepInfra is the embedding provider" |
| Technique or method | `skill` | 0.8 | "Use interpolate() for Remotion animations" |
| Lesson from mistakes | `lesson` | 0.85–0.9 | With trigger/rule/principle fields |
| Other | `other` | 0.5–0.7 | Doesn't fit above categories |

### Importance Scale

| Score | When |
|-------|------|
| 0.3–0.5 | Nice to know, low impact |
| 0.5–0.7 | Useful context (default: 0.7) |
| 0.7–0.85 | Important decision or recurring pattern |
| 0.85–1.0 | Critical — wrong action has serious consequences |

### Confidence-Based Tiering

The Category Reference above gives **default** importance values. Adjust based on how confident the memory is:

| Confidence | Importance | Tier | When to use |
|------------|------------|------|-------------|
| Explicitly stated | 0.9 | `core` | User directly said "I want X", team decision, preference confirmed multiple times |
| Verified in practice | 0.7–0.8 | `working` | Learned from a mistake, technical fact verified by implementation |
| Exploratory | 0.4–0.5 | `peripheral` | One-time question, hypothesis under discussion, unconfirmed direction |

**Rule of thumb**: How many times has this come up?
- Mentioned 3+ times → `core`
- Verified through implementation → `working`
- Mentioned once, still discussing → `peripheral`

---

## Scopes

Memories can be scoped for multi-agent or multi-project setups:

| Format | Use case |
|--------|----------|
| `global` | Shared across all agents/projects |
| `agent:<id>` | Agent-private (default) |
| `project:<id>` | Project-scoped |
| `user:<id>` | User-scoped |

```
memory_store(text: "...", scope: "project:acme")
memory_recall(query: "...", scope: "project:acme")
```

---

## Quick Reference

### Store
```
memory_store(text: "...", category: "fact", importance: 0.7)
```

### Recall
```
memory_recall(query: "database migration strategy", category: "decision", limit: 5)
```

Good queries describe the **situation**, not the exact stored text. Vector search finds semantic matches.

### Update
```
memory_update(memoryId: "a0e8d0fb", text: "Updated: now using OAuth 2.1")
```

For `preference` and `entity`, text changes create a new version (supersede) — history is preserved.

### Merge
```
memory_merge(primaryId: "a0e8d0fb", secondaryId: "3c31e862", mergedText: "Combined memory")
```

### Forget
```
memory_forget(memoryId: "a0e8d0fb")
memory_forget(query: "outdated migration plan")
```

### History
```
memory_history(memoryId: "a0e8d0fb", direction: "both")
```

---

## Setup

Requires [`@cablate/memory-lancedb-mcp`](https://www.npmjs.com/package/@cablate/memory-lancedb-mcp) — see [`mcp.example.json`](../../mcp.example.json) for configuration.
