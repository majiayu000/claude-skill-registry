---
name: compact
description: Compresses context for long sessions by writing state to disk and clearing working memory. Use when context is high/critical or before complex multi-step work.
allowed-tools: Read, Write
---

# Compact

Preserve critical state while freeing context capacity. Writes to disk, clears context, continues with renewed capacity.

## When to Use

- Context status shows High or Critical
- Session running > 60 minutes
- About to start complex multi-step work
- Noticing degraded responses or forgotten instructions

## What Compaction Does

**Before**: Context ~100% saturated
**After**: Context ~50% healthy (state saved to disk)

## Process

1. **Capture State** → Write to `.context/compact-state.md`
2. **Refresh Instructions** → Re-read safety rules, orchestration mode, tools
3. **Acknowledge** → Report compaction complete, ready to continue

## State File Template

```markdown
# Compact State — [timestamp]

## Session Objective
[overall goal]

## Current Task
[what we're working on]

## Completed Work
- [task]: [outcome]

## Key Decisions
- [decision]: [rationale]

## Critical Context
[must-preserve information]

## Next Steps
1. [immediate]
2. [following]
```

## What to Preserve

- Session objective and current task
- Completed work (avoid redoing)
- Key decisions (maintain consistency)
- Blockers and issues
- User preferences expressed

## What to Clear (Safe)

- Exploration that didn't pan out
- Verbose explanations
- Raw file contents (re-read from disk)
- Detailed agent outputs (summary sufficient)

## Output

```markdown
## Context Compacted

**State saved**: `.context/compact-state.md`

### Preserved
- Session objective
- Current task
- Key decisions

### Restored
- Safety rules
- Orchestration mode
- Tool awareness

### Status
**Before**: Critical (~90%)
**After**: Low (~40%)

Ready to continue: [task]
```

## Related

- Emergency compact: See [reference/emergency-compact.md](reference/emergency-compact.md)
- Run first: `/context-status` to determine if needed
- Resume from: `/session-start`
