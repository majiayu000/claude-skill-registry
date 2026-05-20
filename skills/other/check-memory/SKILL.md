---
name: check-memory
description: Explicitly check memory system before answering or exploring
disable-model-invocation: true
---

# Check Memory First

When invoked with `/check-memory <topic>`, this skill forces a memory-first workflow.

## Task

**IMPORTANT: You MUST check memory BEFORE reading any files or running any code searches.**

The user is asking about: $ARGUMENTS

## Step-by-Step Workflow

### 0. Verify Memory Health

Before querying, confirm the memory system is operational:

```
memory.check_setup
```

If status is not "healthy", inform the user and suggest running `claude-memory doctor` for details.

### 1. Query Memory (REQUIRED FIRST STEP)

Run multiple memory queries to find existing knowledge:

```
memory.recall "$ARGUMENTS"
```

Also try specialized shortcuts:
- `memory.decisions` (if implementing a feature)
- `memory.architecture` (if working with frameworks)
- `memory.conventions` (if writing code)
- `memory.conflicts` (if encountering contradictions)

### 2. Analyze Results

Review what memory returns:
- **If sufficient**: Answer using recalled facts with citations
- **If partial**: Note what's known and what needs investigation
- **If empty**: Memory has no knowledge on this topic yet

### 3. Explore Code (ONLY IF NEEDED)

If memory doesn't have enough information:
- Use Read/Grep/Glob to explore the codebase
- Clearly distinguish between:
  - **Recalled knowledge** (from memory)
  - **Discovered information** (from code exploration)

### 4. Provide Complete Answer

Combine:
- Facts from memory (with fact IDs if relevant)
- New information from code exploration (if any)
- Clear indication of sources

## Example Response Format

```
Based on memory:
- [Fact from memory with context]

From code exploration:
- [New findings from reading files]

Answer: [Complete response combining both sources]
```

## Why This Matters

Memory contains distilled knowledge from previous sessions. Checking it first:
- Saves time (no need to re-explore known areas)
- Provides context (decisions, patterns, conventions)
- Avoids mistakes (previous lessons learned)
- Reduces token usage (recalled facts are concise)

## Remember

**ALWAYS start with memory queries. NEVER skip this step.**
