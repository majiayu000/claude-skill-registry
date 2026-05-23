---
name: engram-recall
description: |
  Recall past work from Claude Code history before starting new tasks.
  Use when: (1) starting work on a codebase, (2) asked about previous decisions,
  (3) need context about why code exists.
category: memory
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Glob
---

# Engram Recall

Before diving into implementation, recall relevant context from past sessions.

## When to Use

- Starting work on an existing codebase
- Asked "why was this done this way?"
- Need to understand previous decisions
- Continuing work from a previous session

## Workflow

### Step 1: Check for engram database

```bash
ls .engram/memory.db 2>/dev/null || echo "No engram database found"
```

If no database exists, ingest Claude Code history:

```bash
npx engram ingest-claude --days 14
```

### Step 2: Search for relevant context

Before implementing, search for related decisions:

```bash
npx engram search "your task keywords" --json
```

### Step 3: Review file-specific context

If working on a specific file:

```bash
npx engram context get --file path/to/file.ts --json
```

### Step 4: Document new decisions

After making significant decisions, add context:

```bash
npx engram context add --file path/to/file.ts --note "Chose X over Y because..."
```

## Integration with Other Skills

This skill chains well with:

| Skill | When to Combine |
|-------|-----------------|
| **tdd** | Recall past test patterns before writing tests |
| **code-review** | Check if similar code was reviewed before |
| **describe-codebase** | Augment description with decision history |

## Output Format

When recalling context, format findings as:

```
## Relevant Context Found

**From session [date]:**
- [Summary of decision or discussion]
- Related files: [list]

**Recommendation:** [How this affects current task]
```

## Important

- Don't blindly follow past decisions if they were wrong
- Context is for understanding, not for copy-paste
- Update context when decisions change
