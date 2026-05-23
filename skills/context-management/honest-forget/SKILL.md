---
name: honest-forget
description: Graceful memory compression with integrity — summarize before forgetting, never fabricate
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
  - list_dir
  - search_replace
related: [robust-first, summarize, self-repair, session-log, memory-palace, postel]
tags: [moollm, memory, compression, graceful, context]
inputs:
  target:
    type: path
    required: true
    description: What to potentially forget
  urgency:
    type: enum
    values: [low, medium, high, critical]
    default: medium
    description: How urgently we need to free context
outputs:
  - FORGET.yml
  - WISDOM.yml
  - POINTERS.yml
  - archive/
templates:
  - FORGET.yml.tmpl
  - WISDOM.yml.tmpl
---

# 🌫️ Honest-Forget Skill

> **"Summarize before forgetting. Never fabricate."**

Graceful memory compression that preserves wisdom. Compress context gracefully when budget is exceeded. Extract wisdom, create pointers, and let go with integrity.

## Purpose

Compress context gracefully when budget is exceeded. Extract wisdom, create pointers, and let go with integrity. Never silently lose information or fabricate what was forgotten.

## When to Use

- Context window is filling up
- Completed work needs archiving
- Repetitive iterations need compression
- Old sessions need summarization
- "I've tried this 10 times" situations

## The Honest Forget Cycle

```
ASSESS → EXTRACT → COMPRESS → POINTER → RELEASE
```

## Protocol

### Assessment

Before forgetting, understand what you have:

```yaml
assessment:
  file: "path/to/file.md"
  tokens: 5000
  
  contains:
    decisions: ["List of decisions made"]
    learnings: ["What was learned"]
    questions_answered: ["Q&A pairs"]
    dead_ends: ["What didn't work"]
    
  importance:
    for_current_task: "high|medium|low"
    for_future_reference: "high|medium|low"
```

### Wisdom Extraction

Compress iterations into lessons:

```yaml
wisdom:
  id: "wisdom-001"
  title: "LEARNED: [Pattern/Pitfall]"
  
  compressed_from:
    iterations: "45-55"
    original_tokens: 15000
    
  lesson: |
    The core insight in one paragraph.
    
  pitfalls:
    - "What to avoid"
    
  example:
    good: "What works"
    bad: "What doesn't"
    
  retrieval_hint: |
    When to recall this wisdom:
    - [trigger condition]
```

### Pointer Creation

Leave breadcrumbs for retrieval:

```yaml
pointer:
  to: "path/to/archived/content"
  summary: "One line about what's there"
  
  retrieve_when:
    - "Specific condition"
    
  contains:
    - "What you'll find there"
```

## Schemas

### Assessment Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `file` | ✓ | Path to content |
| `tokens` | ✓ | Size estimate |
| `importance` | ✓ | How critical |
| `decisions` | | Choices made |
| `learnings` | | What was learned |
| `dead_ends` | | Failed approaches |

### Wisdom Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `id` | ✓ | Unique identifier |
| `title` | ✓ | Brief summary |
| `lesson` | ✓ | Core insight |
| `compressed_from` | | Source info |
| `pitfalls` | | What to avoid |
| `example` | | Good/bad examples |
| `retrieval_hint` | | When to recall |

### Pointer Schema

| Field | Required | Purpose |
|-------|----------|---------|
| `to` | ✓ | Archive path |
| `summary` | ✓ | One-line description |
| `retrieve_when` | | Trigger conditions |
| `contains` | | What's there |

## Core Files

| File | Purpose |
|------|---------|
| `FORGET.yml` | Current forgetting session |
| `WISDOM.yml` | Extracted lessons |
| `POINTERS.yml` | Retrieval breadcrumbs |
| `archive/` | Compressed content |

## Commands

| Command | Syntax | Action |
|---------|--------|--------|
| `ASSESS` | `ASSESS [file]` | Evaluate what's there |
| `EXTRACT` | `EXTRACT [wisdom]` | Pull out lessons |
| `COMPRESS` | `COMPRESS [level]` | Create summary |
| `POINTER` | `POINTER [to]` | Leave retrieval hint |
| `RELEASE` | `RELEASE [file]` | Remove from context |

## Compression Levels

| Level | Ratio | Keeps | Use When |
|-------|-------|-------|----------|
| **FULL** | 1:1 | Everything | Still actively needed |
| **WISDOM** | ~5:1 | Lessons, decisions, key facts | Work is done, wisdom remains |
| **SUMMARY** | ~10:1 | Essence and pointers | Background reference only |
| **POINTER** | ~50:1 | Just retrieval hints | Rarely needed, but should remember it exists |

## The Honesty Principle

### What Makes Forgetting "Honest"

**DO:**
- Acknowledge what was forgotten
- Leave pointers for retrieval
- Extract lessons before release
- Document compression decisions

**DON'T:**
- Silently lose information
- Fabricate what was forgotten
- Pretend to remember details
- Hallucinate from partial memory

### When Uncertain

Say: "I compressed earlier iterations. The wisdom I retained is X."

Offer: "I can retrieve the original if needed."

Don't: "Make up details that feel right."

## Working Set

Always include in context:
- `FORGET.yml`
- `WISDOM.yml`
- `POINTERS.yml`

## Dovetails With

### Sister Skills
- [summarize/](../summarize/) — The compression mechanism
- [session-log/](../session-log/) — What to potentially forget
- [self-repair/](../self-repair/) — Triggers forgetting when needed

### Kernel
- [kernel/memory-management-protocol.md](../../kernel/memory-management-protocol.md) — Full specification
