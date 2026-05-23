---
name: rlm-process
description: Process large contexts using RLM (Recursive Language Model) patterns - chunking, filtering, recursive sub-calls
impact: HIGH
impactMetrics:
  - "Handles 100x beyond normal context limits"
  - "28-58% better accuracy on information-dense tasks"
activation:
  patterns:
    - "/rlm"
    - "rlm process"
    - "recursive"
triggers:
  - "rlm"
  - "large context"
  - "process all"
  - "analyze entire"
---

# RLM Process

Process large contexts using Recursive Language Model patterns from arXiv:2512.24601.

## When to Use

Use `/rlm-process` when you need to:
- **Analyze entire codebases** without context overflow
- **Process all pairs/instances** in a dataset
- **Aggregate information** across many files
- **Search through millions of tokens** effectively

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│  RLM Processing Pipeline                                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. ASSESS: Measure context size                            │
│     └─> Determine if RLM needed (>10K tokens)               │
│                                                             │
│  2. FILTER: Search without loading                          │
│     └─> Use grep/glob to narrow relevant content            │
│                                                             │
│  3. CHUNK: Break into processable pieces                    │
│     └─> By file | By section | By line batch                │
│                                                             │
│  4. PROCESS: Recursive sub-calls                            │
│     └─> Each chunk → sub-agent → structured result          │
│                                                             │
│  5. AGGREGATE: Combine results                              │
│     └─> Store in REPL state → synthesize final answer       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Usage

### Basic Usage
```
/rlm-process <query> <context-reference>
```

### Examples

**Codebase Analysis:**
```
/rlm-process "Count all functions that handle authentication" src/
```

**Cross-File Search:**
```
/rlm-process "Find all pairs of files that import the same module" packages/
```

**Large File Processing:**
```
/rlm-process "Summarize each section of this document" large-doc.md
```

**Data Aggregation:**
```
/rlm-process "What labels are most common?" data/questions.jsonl
```

## Invocation

When this skill is invoked, spawn the RLM processor agent:

```
Task tool:
  subagent_type: "rlm-processor"
  model: "sonnet"
  prompt: |
    ## RLM Task
    Query: <user's query>
    Context Reference: <path or reference>

    Use RLM patterns to process this context efficiently.
    Store results in REPL state.
```

## Chunking Strategies

| Strategy | Use When | Example |
|----------|----------|---------|
| `by-file` | Processing codebase | Each .py file separately |
| `by-section` | Document with headers | Each ## section |
| `by-line-batch` | Line-oriented data | 100 lines per batch |
| `pairwise` | Need to compare pairs | All (A,B) combinations |
| `adaptive` | Unknown structure | Let RLM decide |

## Results

Results are stored in REPL state:
```bash
# Check results
python3 ~/.claude/scripts/repl_state.py get rlm_result

# See all chunks
python3 ~/.claude/scripts/repl_state.py list | grep chunk_
```

## When NOT to Use

- **Small contexts** (<10K tokens): Direct read is faster
- **Simple lookups**: Just use grep/read
- **Real-time requirements**: RLM has overhead

## Integration

The `/rlm-process` skill integrates with:
- **REPL State** (`/repl`): Stores intermediate and final results
- **Scout Agent**: Can be used for chunk exploration
- **Worker Agents**: Spawned for parallel chunk processing

## Reference

Based on "Recursive Language Models" (arXiv:2512.24601)
- MIT CSAIL: Alex L. Zhang, Tim Kraska, Omar Khattab
- Key insight: Treat context as environment variable, not neural input

## Session Implementation

When the user invokes this skill:

1. **Parse the query and context reference** from args
2. **Check context size** using file stats or line counts
3. **Spawn rlm-processor agent** with the task
4. **Report results** from REPL state when complete

Example spawn:

```python
# Orchestrator spawns RLM processor
Task(
    subagent_type="rlm-processor",
    model="sonnet",
    prompt=f"""
## RLM Task
Query: {user_query}
Context Reference: {context_ref}
Context Size: {estimated_size}

## Constraints
- Max tokens to read directly: 50000
- Output format: Markdown with citations

Process this context using RLM patterns.
Store final result in REPL state key: rlm_result
""",
    run_in_background=False
)
```
