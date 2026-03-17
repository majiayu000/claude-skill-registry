---
name: worklog
description: "Add timestamped work log entries to track progress and decisions. Use for documenting work, decisions, gotchas, and handoffs between agents."
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Edit, Glob
---

# /worklog

Add structured JSON entries to track work, decisions, and learnings.

## Usage

```bash
/worklog yourbench YB-2 "Added login button to header"
/worklog yourbench YB-2 --decision "Using Clerk for auth"
/worklog yourbench YB-2 --gotcha "Token refresh needs cleanup"
/worklog coordinatr 003 --handoff code-reviewer "Ready for review"
/worklog yourbench YB-2 --state              # Show current state
/worklog yourbench YB-2 --migrate            # Migrate from WORKLOG.md
```

## Directory Structure

```
ideas/yourbench/issues/YB-2-auth/
├── TASK.md
├── PLAN.md
└── worklog/
    ├── _state.json              # Current state (quick context load)
    ├── 001-phase-init.json      # Entry files
    └── 002-handoff-review.json
```

## Entry Types

| Type | Flag | Use Case |
|------|------|----------|
| Manual | (default) | General progress update |
| Decision | `--decision` | Document architectural choice |
| Gotcha | `--gotcha` | Capture lesson learned |
| Handoff | `--handoff TO` | Agent transition |
| Phase | `--phase NUM` | Phase completion |
| Blocker | `--blocker` | Record impediment |
| Resolution | `--resolve ID` | Resolve blocker |

## Execution Flow

### 1. Parse Arguments

```
/worklog PROJECT ISSUE_ID [--type] "message"
```

### 2. Locate Worklog Directory

```bash
ideas/[project]/issues/[issue_id]-*/worklog/
mkdir -p [path] if missing
```

### 3. Get Next Sequence Number

```bash
ls worklog/*.json | grep -v _state | wc -l
# Next = count + 1
```

### 4. Create Entry File

Filename: `{sequence:03d}-{type}-{slug}.json`

**Required fields:**
- `$schema`: "worklog-entry-v1"
- `id`: "ISSUE-SEQ"
- `sequence`: number
- `timestamp`: ISO 8601
- `type`: entry type
- `author`: { agent: string | null, human: string | null }
- `summary`: description

### 5. Update `_state.json`

After every entry:
- Update `last_entry`
- Update `last_updated`
- Increment `entries_count`
- Add to `key_decisions` if decision
- Update `blockers` if blocker/resolution

## Viewing State

```bash
/worklog yourbench YB-2 --state
```

Outputs:
```
Issue: YB-2 - Initialize Next.js project
Status: in_progress (Phase 3)
Progress: 5/5 phases complete
Key Decisions: ...
Blockers: none
```

## Schema Reference

See [references/schema.md](references/schema.md) for full JSON schema specification.

## Best Practices

1. **Be specific**: Include enough context for future AI
2. **Tag consistently**: Use established tag taxonomy
3. **Capture gotchas immediately**: Don't wait until end
4. **Handoff explicitly**: Create handoff entry when switching agents
5. **Update state**: `_state.json` should always reflect current reality
