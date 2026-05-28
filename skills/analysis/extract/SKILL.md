---
name: extract
description: 'Extract decisions and learnings from Claude session transcripts. Triggers: "extract learnings", "process pending", SessionStart hook.'
---

# Extract Skill

**Typically runs automatically via SessionStart hook.**

Process pending learning extractions from previous sessions.

## How It Works

The SessionStart hook runs:
```bash
ao extract
```

This checks for queued extractions and outputs prompts for Claude to process.

## Manual Execution

Given `/extract`:

### Step 1: Check for Pending Extractions

```bash
ao extract 2>/dev/null
```

Or check the pending queue:
```bash
cat .agents/ao/pending.jsonl 2>/dev/null | head -5
```

### Step 2: Process Each Pending Item

For each queued session:
1. Read the session summary
2. Extract actionable learnings
3. Write to `.agents/learnings/`

### Step 3: Write Learnings

**Write to:** `.agents/learnings/YYYY-MM-DD-<session-id>.md`

```markdown
# Learning: <Short Title>

**ID**: L1
**Category**: <debugging|architecture|process|testing|security>
**Confidence**: <high|medium|low>

## What We Learned

<1-2 sentences describing the insight>

## Why It Matters

<1 sentence on impact/value>

## Source

Session: <session-id>
```

### Step 4: Clear the Queue

```bash
ao extract --clear 2>/dev/null
```

### Step 5: Report Completion

Tell the user:
- Number of learnings extracted
- Key insights
- Location of learning files

## The Knowledge Loop

```
Session N ends:
  → ao forge --last-session --queue
  → Session queued in pending.jsonl

Session N+1 starts:
  → ao extract (this skill)
  → Claude processes the queue
  → Writes to .agents/learnings/
  → Loop closed
```

## Key Rules

- **Runs automatically** - usually via hook
- **Process the queue** - don't leave extractions pending
- **Be specific** - actionable learnings, not vague observations
- **Close the loop** - extraction completes the knowledge cycle
