---
name: claude-restart-compact
description: Compact context at natural breakpoints to free tokens and continue working. Use PROACTIVELY at phase boundaries, after commits, or when token usage >150k. Better than random auto-compact. Supports custom compaction prompts.
---

Compacting context at natural breakpoint and resuming work...

This will:
- Summarize recent conversation to free tokens
- Preserve task context and state
- Resume with compact history
- Continue working on current task

## When to Use (Natural Breakpoints)

Use at **logical stopping points** rather than letting Claude auto-compact randomly:

**After completing a phase:**
- Feature implementation done and committed
- Test suite passing
- Documentation updated
- Natural transition to next phase

**At project boundaries:**
- Completed one component, starting another
- Finished refactoring, moving to new feature
- After major milestone

**Before running out of space:**
- Token usage >150k (75% of 200k budget)
- Long conversations (>100 messages)
- Before starting large multi-phase work

**Benefits over auto-compact:**
- Control WHEN compaction happens
- Compact at meaningful boundaries
- Preserve important context
- Custom prompts guide what to keep

## Usage

**Basic** (default compaction):
```bash
.claude/skills/claude-restart-resume/scripts/claude-restart.sh compact
```

**With custom prompt** (guides what to preserve):
```bash
# Set compaction prompt before invoking
export COMPACT_PROMPT="Preserve: API design decisions, database schema, known bugs"
.claude/skills/claude-restart-resume/scripts/claude-restart.sh compact
```

## Compaction Prompts

Custom prompts help preserve important context:

```bash
# Keep technical decisions
COMPACT_PROMPT="Preserve architectural decisions and open technical questions"

# Keep project state
COMPACT_PROMPT="Preserve TODO list state, recent commits, and next steps"

# Keep domain knowledge
COMPACT_PROMPT="Preserve domain model, business rules, and API contracts"
```

The script will pass this to Claude during compaction to guide summarization.
