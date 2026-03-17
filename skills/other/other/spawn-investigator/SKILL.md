---
name: spawn-investigator
description: Investigate a codebase question using an isolated subagent. Use when you need to read many files without bloating the main context.
argument-hint: [question to investigate]
---

# Spawn Investigator

Launch an isolated investigation subagent to answer a codebase question without polluting the main conversation context.

## Why This Exists

Reading many files to answer a question fills up the main context window. By spawning an Explore-type subagent, the investigation happens in a separate context. Only the concise answer comes back, keeping the main context clean for actual work.

## Usage

- `/spawn-investigator <question>` — User-invoked investigation
- Claude can also auto-invoke this when it recognizes a question requiring broad codebase exploration

## Procedure

### Step 1: Formulate the Question

Parse `$ARGUMENTS` into a clear, specific investigation question. If the question is vague, refine it:

- BAD: "How does auth work?"
- GOOD: "What authentication middleware is used, where is it configured, and what are the auth routes?"

### Step 2: Spawn the Subagent

Use the Task tool with these parameters:

```
subagent_type: Explore
description: "Investigate: [short summary]"
prompt: |
  Investigate this question about the codebase:

  **Question:** [the question]

  Instructions:
  - Search broadly first (Glob for file patterns, Grep for keywords)
  - Read the most relevant files
  - Trace the code path if needed (follow imports, function calls)
  - Return a CONCISE answer (max 500 words) with:
    1. Direct answer to the question
    2. Key file paths discovered
    3. Any important caveats or gotchas
  - Do NOT include full file contents in your response
```

### Step 3: Report Back

When the subagent returns, present the findings to the user:

```
## Investigation Results: [question summary]

[Subagent's concise answer]

### Key Files
- `path/to/file1` — [what it does]
- `path/to/file2` — [what it does]
```

If the answer is insufficient, offer to spawn a follow-up investigator with a more specific question.

## When to Auto-Invoke

Claude should consider auto-invoking this skill when:
- The user asks a broad "how does X work?" question
- Answering requires reading 5+ files
- The main context is already large (approaching compaction)
- The question is about understanding, not modifying, code
