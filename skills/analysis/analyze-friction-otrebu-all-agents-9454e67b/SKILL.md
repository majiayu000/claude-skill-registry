---
name: analyze-friction
description: Orchestrate 3-stage friction analysis workflow across conversations. Extracts raw friction, abstracts patterns, and presents for approval. Use when user wants to analyze conversation history for improvement opportunities.
allowed-tools: Task, Bash, Read, Glob, AskUserQuestion
---

# Friction Analysis Orchestrator

Orchestrates a 3-stage workflow to analyze conversation friction and extract actionable patterns.

## Arguments

- `--count N` - Number of conversations to analyze (default: 15)

## Overview

| Stage | Agent | Purpose |
|-------|-------|---------|
| 1 | conversation-friction-analyzer | Extract raw friction from individual conversations (parallel) |
| 2 | friction-pattern-abstractor | Aggregate and abstract patterns across all raw outputs |
| 3 | (orchestrator) | Present patterns to user for point-by-point approval |

## Workflow

### Stage 0: Preparation

1. Parse arguments for `--count N` (default 15)
2. Check existing files in `docs/friction-analysis/raw/` to determine which conversations are already processed
3. Calculate which conversations need analysis (skip index 0 - current session)

```bash
# List existing raw files
ls docs/friction-analysis/raw/ 2>/dev/null || echo "No existing files"
```

### Stage 1: Raw Friction Extraction (Parallel)

For each conversation index from 1 to N (skipping 0 which is current session):

1. Check if `docs/friction-analysis/raw/{conversation-id}.md` already exists
2. If not exists, spawn a `conversation-friction-analyzer` agent:

```
Spawn agents in parallel (up to 15 concurrent):

For conversation at index I (where I = 1 to count):
  - Extract conversation: `aaa extract-conversations --limit 1 --skip I`
  - Pass to conversation-friction-analyzer agent
  - Agent saves output to docs/friction-analysis/raw/{conversation-id}.md
```

**Sub-agent prompt template:**

```
Analyze this conversation for friction points. Extract RAW friction only - no abstraction.

CONVERSATION:
<output from aaa extract-conversations --limit 1 --skip {index}>

Save your analysis to: docs/friction-analysis/raw/{conversation-id}.md
```

**Resumability:** Always check for existing files before spawning agents. Skip conversations that already have raw output files.

### Stage 2: Pattern Abstraction (Sequential)

After ALL Stage 1 agents complete:

1. Verify all expected raw files exist in `docs/friction-analysis/raw/`
2. Spawn single `friction-pattern-abstractor` agent:

```
Analyze all raw friction files and extract patterns.

Input directory: docs/friction-analysis/raw/
Output file: docs/friction-analysis/patterns.md
```

Wait for completion before proceeding.

### Stage 3: User Approval

1. Read the generated `docs/friction-analysis/patterns.md`
2. For EACH pattern identified, use AskUserQuestion to get approval:

```
Pattern: [Pattern Name]
Root Cause: [description]
Evidence: [list of conversation IDs]
Proposed Fix: [description]

Options:
- Approve - proceed with this fix
- Modify - adjust the proposed fix
- Skip - don't implement this pattern
- Stop - end the approval process
```

3. Collect approved patterns
4. Output summary of approved patterns for implementation

## Output Structure

```
docs/friction-analysis/
├── raw/
│   ├── {conversation-id-1}.md    # Stage 1 output
│   ├── {conversation-id-2}.md
│   └── ...
└── patterns.md                    # Stage 2 output
```

## Error Handling

- If `aaa extract-conversations` fails for a conversation, log and continue with others
- If Stage 1 produces no raw files, abort with message "No friction found to analyze"
- If Stage 2 fails, check raw files exist and retry

## Completion

After Stage 3, output:

```markdown
## Friction Analysis Complete

**Analyzed:** N conversations
**Patterns Found:** M
**Patterns Approved:** K

### Approved Patterns

1. [Pattern Name] - [Proposed Fix Summary]
2. ...

### Next Steps

[Implementation guidance for approved patterns]
```
