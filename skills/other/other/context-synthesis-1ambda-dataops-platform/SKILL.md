---
name: context-synthesis
description: Token-efficient context gathering and synthesis from multiple sources (memory, docs, web). Orchestrates MCP tools to build comprehensive context before analysis or interviews. Use when starting discovery, research, or analysis tasks.
---

# Context Synthesis

Efficient multi-source context gathering that minimizes token usage while maximizing relevant information.

## When to Use

- Starting stakeholder discovery/interviews
- Researching new features or domains
- Building context for analysis tasks
- Synthesizing information from multiple sources

## Core Principle

> **Gather silently, synthesize briefly, share relevantly.**

Token efficiency comes from:
1. Parallel MCP tool calls (not sequential)
2. Filtering irrelevant results before presenting
3. Structured summaries over raw dumps

---

## Context Gathering Pattern

### Step 1: Parallel Information Retrieval

Execute these in parallel (single tool call block):

```python
# All four in parallel - not sequential
mcp__plugin_claude-mem_mem-search__search(query="{keyword}")
mcp__serena__list_memories()
Glob(pattern="**/features/*_FEATURE.md")
WebSearch(query="{domain} best practices 2025")
```

### Step 2: Selective Deep Reads

Based on Step 1 results, read only high-relevance items:

```python
# Only if memory mentions relevant topic
mcp__serena__read_memory(memory_file_name="relevant_memory")

# Only if glob found matching specs
Read(file_path="/path/to/relevant/*_FEATURE.md")

# Only if search returned actionable results
WebFetch(url="most_relevant_url", prompt="extract specific info")
```

### Step 3: Structured Synthesis

Present findings in structured format:

```markdown
**Context Summary** ({feature/topic})

| Source | Key Finding | Relevance |
|--------|-------------|-----------|
| Memory | Past decision X | Direct |
| Spec FEATURE_A | Similar pattern Y | Reference |
| Web | Industry trend Z | Background |

**Implications for Current Task:**
- [Key implication 1]
- [Key implication 2]
```

---

## Source Priority Order

| Priority | Source | When to Use | Token Cost |
|----------|--------|-------------|------------|
| 1 | claude-mem | Always first | Low |
| 2 | serena memories | Project context | Low |
| 3 | Existing specs | Pattern reference | Medium |
| 4 | WebSearch | Industry context | Medium |
| 5 | WebFetch | Deep dive needed | High |

---

## Anti-Patterns

| Anti-Pattern | Problem | Better Approach |
|--------------|---------|-----------------|
| Sequential tool calls | Slow, inefficient | Parallel execution |
| Reading all files | Token waste | Selective deep reads |
| Dumping raw results | Cognitive overload | Structured synthesis |
| Skipping memory check | Miss past decisions | Always check first |
| WebFetch everything | High token cost | Only for high-value URLs |

---

## Integration with Other Skills

### With requirements-discovery
```
1. context-synthesis gathers background
2. requirements-discovery conducts interview
3. Context informs question prioritization
```

### With architecture
```
1. context-synthesis gathers existing patterns
2. architecture analyzes against patterns
3. Context validates decisions
```

---

## Quick Reference

```python
# Minimal context check (fast)
mcp__plugin_claude-mem_mem-search__search(query="{topic}")
mcp__serena__list_memories()

# Standard context gathering (balanced)
# Add: Glob for existing specs, WebSearch for trends

# Deep context research (comprehensive)
# Add: WebFetch for detailed sources, multiple memory reads
```
