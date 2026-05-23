---
name: inject
description: 'Inject relevant knowledge into session context from .agents/ artifacts. Triggers: "inject knowledge", "recall context", SessionStart hook.'
---

# Inject Skill

**Typically runs automatically via SessionStart hook.**

Inject relevant prior knowledge into the current session.

## How It Works

The SessionStart hook runs:
```bash
ao inject --apply-decay --format markdown --max-tokens 1000
```

This searches for relevant knowledge and injects it into context.

## Manual Execution

Given `/inject [topic]`:

### Step 1: Search for Relevant Knowledge

**With ao CLI:**
```bash
ao inject --context "<topic>" --format markdown --max-tokens 1000
```

**Without ao CLI, search manually:**
```bash
# Recent learnings
ls -lt .agents/learnings/ | head -5

# Recent patterns
ls -lt .agents/patterns/ | head -5

# Recent research
ls -lt .agents/research/ | head -5
```

### Step 2: Read Relevant Files

Use the Read tool to load the most relevant artifacts based on topic.

### Step 3: Summarize for Context

Present the injected knowledge:
- Key learnings relevant to current work
- Patterns that may apply
- Recent research on related topics

## Knowledge Sources

| Source | Location | Priority |
|--------|----------|----------|
| Learnings | `.agents/learnings/` | High |
| Patterns | `.agents/patterns/` | High |
| Research | `.agents/research/` | Medium |
| Retros | `.agents/retros/` | Medium |

## Decay Model

Knowledge relevance decays over time (~17%/week). More recent learnings are weighted higher.

## Key Rules

- **Runs automatically** - usually via hook
- **Context-aware** - filters by current directory/topic
- **Token-budgeted** - respects max-tokens limit
- **Recency-weighted** - newer knowledge prioritized
