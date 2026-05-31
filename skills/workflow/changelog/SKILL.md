---
name: changelog
description: View and manage the runtime changelog for observability
user-invocable: true
---

# Changelog Skill

> **Status: Experimental**
> This feature uses Claude Code's PostToolUse hooks. The hook interface may change in future versions.
> If hooks don't trigger as expected, events can still be logged manually via auto-loop prompts.

Runtime observability changelog for tracking all changes during development sessions.

---

## Overview

This skill provides an **automated** changelog system that:
- **Automatically** records file changes via PostToolUse hooks
- **Automatically** logs test results when tests are run
- **Automatically** records git commits
- **Automatically** rotates when exceeding 500 lines
- Enables subagents to understand context from previous actions
- Supports session recovery and debugging

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Observability System                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐     ┌─────────────────────────────┐           │
│  │ Write/Edit  │     │           Bash              │           │
│  │    Tool     │     │   (test/commit/general)     │           │
│  └──────┬──────┘     └──────────────┬──────────────┘           │
│         │                           │                           │
│         ▼                           ▼                           │
│  ┌─────────────────────────────────────────────────────┐       │
│  │              PostToolUse Hooks                       │       │
│  │     log-file-change.sh       log-bash-event.sh      │       │
│  └─────────────────────────┬───────────────────────────┘       │
│                            │                                    │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────┐       │
│  │           _lib-changelog.sh                        │       │
│  │  • log_event()      • rotate_if_needed()            │       │
│  │  • archive_changelog()  • clear_changelog()         │       │
│  └─────────────────────────┬───────────────────────────┘       │
│                            │                                    │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────┐       │
│  │         .director-mode/changelog.jsonl               │       │
│  │                                                      │       │
│  │  {"event_type":"file_created",...}                  │       │
│  │  {"event_type":"test_pass",...}                     │       │
│  │  {"event_type":"commit",...}                        │       │
│  └─────────────────────────────────────────────────────┘       │
│                            │                                    │
│              ┌─────────────┴─────────────┐                     │
│              ▼                           ▼                     │
│  ┌─────────────────┐         ┌─────────────────┐               │
│  │  /changelog     │         │    Subagents    │               │
│  │   command       │         │ code-reviewer   │               │
│  │                 │         │ debugger        │               │
│  └─────────────────┘         └─────────────────┘               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Relationship with Checkpoint

| Aspect | Checkpoint | Changelog |
|--------|------------|-----------|
| Location | `.auto-loop/checkpoint.json` | `.director-mode/changelog.jsonl` |
| Purpose | Current state snapshot | Historical event stream |
| Question answered | "Where am I now?" | "How did I get here?" |
| Used by | Stop Hook (continue/stop decision) | Subagents (context) |
| Format | Single JSON object | JSONL (append-only) |
| Persistence | Overwritten each iteration | Accumulated, then rotated |

**They complement each other:**
- **Checkpoint** = Save point for resume
- **Changelog** = Audit trail for observability

---

## Automatic Logging via Hooks

### Hook Configuration (`.claude/settings.local.json`)

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-file-change.sh" }]
      },
      {
        "matcher": "Edit",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-file-change.sh" }]
      },
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/log-bash-event.sh" }]
      }
    ]
  }
}
```

> **Note**: Uses `$CLAUDE_PROJECT_DIR` for portable paths (resolved at runtime by Claude Code).

### Hook Scripts

| Script | Trigger | Events Logged |
|--------|---------|---------------|
| `log-file-change.sh` | Write, Edit | `file_created`, `file_modified` |
| `log-bash-event.sh` | Bash | `test_pass`, `test_fail`, `commit` |

---

## Automatic Rotation

**Prevents unbounded growth:**

```bash
MAX_LINES=500

# When changelog exceeds 500 lines:
# 1. Move current to changelog.YYYYMMDD_HHMMSS.jsonl
# 2. Start fresh changelog.jsonl
# 3. Log rotation event
```

**Result:**

```
.director-mode/
├── changelog.jsonl                    ← Current (< 500 lines)
├── changelog.20250113_103000.jsonl    ← Archived
├── changelog.20250112_150000.jsonl    ← Archived
└── changelog.20250111_090000.jsonl    ← Archived
```

---

## Session Conflict Prevention

**Only one auto-loop session per project:**

```bash
# When starting /auto-loop:
if checkpoint exists AND status == "in_progress":
    → Block with message:
      "Found interrupted session at iteration #N"
      "Use --resume or --force"
```

**Options:**
- `/auto-loop --resume` → Continue with existing checkpoint + changelog
- `/auto-loop --force "task"` → Archive old, start fresh

---

## Event Schema

```json
{
  "id": "evt_1705142400_12345",
  "timestamp": "2025-01-13T10:30:00.000Z",
  "event_type": "file_modified",
  "agent": "hook",
  "iteration": 3,
  "summary": "file_modified: Login.tsx",
  "files": ["src/components/Login.tsx"]
}
```

### Event Types

| Type | Source | Description |
|------|--------|-------------|
| `file_created` | Hook (Write) | New file created |
| `file_modified` | Hook (Edit) | File edited |
| `test_pass` | Hook (Bash) | Tests passing |
| `test_fail` | Hook (Bash) | Tests failing |
| `commit` | Hook (Bash) | Git commit made |
| `session_start` | auto-loop | Session begins |
| `session_end` | auto-loop | Session completes |
| `changelog_rotated` | System | Changelog was rotated |

---

## Subagent Integration

### code-reviewer

Before review, checks changelog for:
- What files were changed recently
- What iteration we're on
- Recent test results

### debugger

Before debugging, checks changelog for:
- When errors first occurred
- What files changed before errors
- Pattern of test failures

---

## Core Functions (`_lib-changelog.sh`)

```bash
# Log an event
log_event "file_created" "Created Login.tsx" "hook" '["src/Login.tsx"]'

# Archive current changelog
archive_changelog

# Clear changelog
clear_changelog

# List archives
list_archives
```

---

## Querying

### Via Command

```bash
/changelog                  # Recent 10 events
/changelog --summary        # Statistics
/changelog --type test      # Filter by type
/changelog --list-archives  # Show old changelogs
/changelog --export log.json
```

### Via Bash

```bash
# Last 5 events
tail -n 5 .director-mode/changelog.jsonl | jq '.'

# All file changes
grep '"event_type":"file_' .director-mode/changelog.jsonl

# Count by type
jq -r '.event_type' .director-mode/changelog.jsonl | sort | uniq -c
```

---

## Example Session Flow

```
1. /auto-loop "Implement login"
   → Check: No existing session
   → Archive old changelog (if > 100 lines)
   → Create checkpoint (status: in_progress)
   → Log: session_start

2. TDD Iteration #1
   → Write test file
   → Hook logs: file_created
   → Run tests (fail)
   → Hook logs: test_fail
   → Write implementation
   → Hook logs: file_created
   → Run tests (pass)
   → Hook logs: test_pass
   → Commit
   → Hook logs: commit

3. Session interrupted (crash/exit)
   → Checkpoint remains: iteration=1, status=in_progress
   → Changelog has full history

4. /auto-loop "something"
   → Check: Found in_progress session!
   → Block: "Use --resume or --force"

5. /auto-loop --resume
   → Read checkpoint: iteration=1
   → Read changelog: understand context
   → Continue from iteration #2
```

---

## Installation

Hooks are installed with Director Mode Lite:

```bash
# After install, verify:
ls .claude/hooks/
# → auto-loop-stop.sh
# → _lib-changelog.sh
# → log-bash-event.sh
# → log-file-change.sh
# → pre-tool-validator.sh

cat .claude/settings.local.json | jq '.hooks'
```

---

## Troubleshooting

### Events not logged

1. Check hooks exist: `ls .claude/hooks/*.sh`
2. Check hooks.json: `cat hooks/hooks.json`
3. Check scripts are executable: `chmod +x .claude/hooks/*.sh`

### Stale session blocking

```bash
# Check what's there
cat .auto-loop/checkpoint.json | jq '.status'

# Force restart
/auto-loop --force "New task"
```

### Changelog too large

```bash
# Manual archive
/changelog --archive

# Or clear
/changelog --clear
```
