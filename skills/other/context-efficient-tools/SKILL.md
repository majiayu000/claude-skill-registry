---
name: context-efficient-tools
description: Filter and transform tool results before they reach the model — prevent context bloat from large outputs
category: Workflow Orchestration
---

# Skill: context-efficient-tools

## What I do

I prevent large tool results from bloating the context window. When tools return large datasets, I apply filtering, aggregation, and summarisation in code before the result reaches the model. Anthropic found this reduces token usage by up to 98.7% on large MCP tool chains.

## When to use me

- When MCP tools might return large datasets (files, search results, database queries)
- When chaining multiple tool calls with large intermediate results
- When bash commands produce verbose output
- When token budget is constrained and tool results are the bottleneck

## Core principles

1. **Filter before returning** — Never pass raw large results to the model
2. **Summarise, don't dump** — Return counts + samples, not full datasets
3. **Store externally, reference internally** — Write large results to files, pass the path
4. **Progressive disclosure** — Start with metadata, drill down only if needed
5. **Code does the work** — Use bash/scripts to process, not the model

## Patterns

### Large file reading
```bash
# Bad: model sees entire file
cat large_config.json

# Good: extract only what's needed
jq '.database' large_config.json
grep -A5 "relevant_key" large_config.json
```

### Search results
```bash
# Bad: 500 matches flood context
grep -r "pattern" .

# Good: count + sample + file list
grep -r "pattern" . | wc -l
grep -r "pattern" . | head -10
grep -rl "pattern" .
```

### Large dataset filtering
```bash
# Bad: all 10,000 rows
cat data.csv

# Good: summary + sample
wc -l data.csv && head -5 data.csv
awk -F',' '$3 == "pending"' data.csv | head -10
```

### Storing large outputs
```bash
# Store externally, return reference + metadata
some_tool > /tmp/output.txt
echo "Stored $(wc -l < /tmp/output.txt) lines → /tmp/output.txt"
head -5 /tmp/output.txt
```

### Build/install output
```bash
# Bad: full verbose output
npm install

# Good: errors and warnings only
npm install 2>&1 | grep -E "error|warn|ERR" | head -20
echo "Exit: $?"
```

## Decision matrix

| Result size    | Action                                      |
|----------------|---------------------------------------------|
| < 50 lines     | Pass directly                               |
| 50–500 lines   | Filter to relevant subset                   |
| 500–5000 lines | Summarise + sample + store to file          |
| > 5000 lines   | Store to file, pass path + metadata only    |

## Anti-patterns to avoid

- ❌ `cat` on files > 100 lines without filtering
- ❌ Passing full grep output when count + sample suffices
- ❌ Reading entire JSON configs when only one key is needed
- ❌ Letting verbose build output fill context
- ❌ Passing intermediate tool results verbatim to the next tool call

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Session-Knowledge/Context Efficient Tools.md`

## Related skills

- `token-efficiency` — Prompt-level efficiency (complements this skill)
- `scope-management` — Scope determines which tools are called
- `parallel-execution` — Run independent tool calls simultaneously
- `performance` — Efficient data processing patterns
