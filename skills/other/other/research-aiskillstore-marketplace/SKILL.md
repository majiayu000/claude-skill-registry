---
name: research
description: Multi-source parallel research with confidence-based synthesis.
---

# Research Skill

Multi-source parallel research with confidence-based synthesis.

## Trigger Phrases

When user asks:
- "research X for me"
- "find out about X"
- "what's the current status of X"
- "gather information on X"
- "deep dive into X"

## Quick Reference

| Mode | Speed | Depth | Use Case |
|------|-------|-------|----------|
| quick | ~30s | Shallow | Fact check, simple lookup |
| standard | ~2min | Moderate | Typical research |
| extensive | ~8min | Deep | Comprehensive analysis |

## Command

```
/ai-dev-kit:research [mode] [query]
```

## Mode Selection

```
Need quick answer? ─────────────► quick
  │
  ├─ Need current info? ────────► standard
  │
  └─ Need comprehensive? ───────► extensive
```

## Research Types

| Type | Sources | Best For |
|------|---------|----------|
| Web | WebSearch | Current events, latest docs |
| Docs | Local ai-docs/ | Library usage, patterns |
| Code | Codebase grep | Implementation examples |

## Confidence Levels

| Level | Meaning | Source Count |
|-------|---------|--------------|
| HIGH | Very reliable | 3+ agree |
| MEDIUM | Likely accurate | 2 agree |
| LOW | Needs verification | 1 only |
| CONFLICTING | Check manually | Sources disagree |

## Cookbook

- `cookbook/quick-mode.md` - Fast fact-checking pattern
- `cookbook/standard-mode.md` - Balanced research pattern
- `cookbook/extensive-mode.md` - Deep research pattern

## Reference

- `reference/researcher-types.md` - Available researcher agents
- `reference/synthesis-patterns.md` - How findings are combined

## Common Gotchas

- **Timeout**: Extensive mode may timeout on slow connections. Results are still returned.
- **Docs only**: If web is down, doc-only results are returned with note.
- **Conflicting info**: Review "Conflicting Information" section when present.
