---
name: research-cache
description: Caches research findings to avoid redundant web searches. Stores best practices by topic with sources and dates. Use before researching to check existing knowledge.
allowed-tools: Read, Write, Glob, Grep
---

# Research Cache - Best Practices Storage

## Purpose

This skill caches research findings to avoid redundant web searches and maintain institutional knowledge about best practices.

---

## Structure

```
.claude/skills/research-cache/
├── SKILL.md          # This file
├── TEMPLATE.md       # Template for research findings
└── cache/            # Cached research by topic
    ├── solana-websockets.md
    ├── typescript-strict.md
    └── [topic].md
```

---

## How It Works

### Before Research

1. **Check cache first** - Look for existing research on the topic
2. **Verify freshness** - Research older than 6 months may need updating
3. **Reuse findings** - If recent research exists, use it directly

### After Research

1. **Create cache file** - Document findings in `cache/[topic].md`
2. **Follow template** - Use consistent structure
3. **Include sources** - Always cite URLs and dates
4. **Tag relevance** - Mark which parts of stack it applies to

---

## Cache File Template

````markdown
# Research: [Topic Name]

## Metadata

- **Date:** YYYY-MM-DD
- **Researcher:** [agent/session]
- **Freshness:** [fresh|stale|outdated]
- **Stack:** [bun|typescript|mongodb|solana|all]

## Problem Statement

[What problem were we trying to solve?]

## Search Queries

1. "[query 1]"
2. "[query 2]"
3. "[query 3]"

## Key Findings

### Finding 1: [Title]

**Source:** [URL]
**Date:** [publication date]
**Relevance:** [high|medium|low]

[Summary of finding]

**Code Example:**

```[language]
[code]
```
````

**Applies When:**

- [condition 1]
- [condition 2]

### Finding 2: [Title]

...

## Recommendations

### DO

1. [Best practice 1]
2. [Best practice 2]

### AVOID

1. [Anti-pattern 1]
2. [Anti-pattern 2]

### CONSIDER

1. [Alternative approach 1]
2. [Alternative approach 2]

## Implementation Notes

### For This Project

- [Specific note for solana-listeners]
- [Integration point]

### Gotchas

- [Warning 1]
- [Warning 2]

## Sources

| Title      | URL   | Date   | Relevance      |
| ---------- | ----- | ------ | -------------- |
| [Source 1] | [url] | [date] | [high/med/low] |
| [Source 2] | [url] | [date] | [high/med/low] |

## Related Topics

- [[related-topic-1]]
- [[related-topic-2]]

````

---

## Usage Patterns

### Quick Lookup

```bash
# Check if research exists
ls .claude/skills/research-cache/cache/

# Read specific research
cat .claude/skills/research-cache/cache/[topic].md
````

### Search Cached Research

```bash
# Find all research mentioning a term
grep -r "websocket" .claude/skills/research-cache/cache/
```

### Check Freshness

```bash
# Find research older than 6 months
find .claude/skills/research-cache/cache/ -mtime +180
```

---

## Integration with Research Agent

The **research agent** uses this skill to:

1. **Check existing research** before web searching
2. **Store new findings** after web research
3. **Update stale research** when patterns change
4. **Cross-reference** findings across topics

---

## Freshness Guidelines

| Age         | Status   | Action                  |
| ----------- | -------- | ----------------------- |
| < 3 months  | Fresh    | Use directly            |
| 3-6 months  | Aging    | Verify still valid      |
| 6-12 months | Stale    | Update recommended      |
| > 12 months | Outdated | Full re-research needed |

---

## Topic Naming Convention

Use kebab-case descriptive names:

```
solana-websockets.md       # Technology + feature
typescript-strict-mode.md  # Language + specific setting
mongodb-indexes.md         # Database + concept
bun-docker-deploy.md       # Runtime + deployment context
error-handling-patterns.md # Generic pattern
```

---

## Rules

### MANDATORY

1. **Always check cache first** - Don't duplicate research
2. **Always include sources** - No unsourced recommendations
3. **Always date entries** - Freshness matters
4. **Always follow template** - Consistency helps retrieval

### FORBIDDEN

1. **Cache without sources** - All findings need citations
2. **Ignore freshness** - Old research may be wrong
3. **Duplicate topics** - One file per topic, update existing

---

## Version

- **v1.0.0** - Initial implementation
