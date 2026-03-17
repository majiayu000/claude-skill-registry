---
name: session-inspector
description: >
  This skill should be used when inspecting, analyzing, or querying Claude Code session logs.
  Use when users ask about session history, want to find sessions, analyze context usage,
  extract tool call patterns, debug agent execution, or understand what happened in previous
  sessions. Essential for understanding Claude Code's ~/.claude/projects/ structure, JSONL
  session format, and the erk extraction pipeline.
---

# Session Inspector

## Overview

Session Inspector provides comprehensive tools for inspecting Claude Code session logs stored
in `~/.claude/projects/`. The skill enables:

- Discovering and listing sessions for any project/worktree
- Preprocessing sessions to readable XML format
- Analyzing context window consumption
- Extracting plans from sessions
- Creating GitHub issues from session content
- Debugging agent subprocess execution
- Understanding the two-stage extraction pipeline

## When to Use

Invoke this skill when users:

- Ask what sessions exist for a project or worktree
- Want to find a specific session by ID or content
- Need to analyze context window consumption
- Ask about tool call patterns or frequencies
- Need to debug agent subprocess failures
- Want to extract plans from sessions
- Ask about session history or previous conversations
- Need to understand session preprocessing or extraction

## Quick Reference: CLI Commands

All commands invoked via `erk exec <command>`:

| Command                      | Purpose                                          |
| ---------------------------- | ------------------------------------------------ |
| `list-sessions`              | List sessions with metadata for current worktree |
| `preprocess-session`         | Convert JSONL to compressed XML                  |
| `extract-latest-plan`        | Extract most recent plan from session            |
| `create-issue-from-session`  | Create GitHub issue from session plan            |
| `extract-session-from-issue` | Extract session content from GitHub issue        |

### Slash Commands

| Command                  | Purpose                                      |
| ------------------------ | -------------------------------------------- |
| `/erk:sessions-list`     | Display formatted session list table         |
| `/local:analyze-context` | Analyze context window usage across sessions |

## Core Capabilities

### 1. List Sessions

```bash
erk exec list-sessions [--limit N] [--min-size BYTES]
```

**Options:**

- `--limit`: Maximum sessions to return (default: 10)
- `--min-size`: Minimum file size in bytes to filter tiny sessions (default: 0)

**Output includes:**

- Branch context (current_branch, trunk_branch, is_on_trunk)
- Current session ID from SESSION_CONTEXT env var
- Sessions array with: session_id, mtime_display, mtime_relative, size_bytes, summary, is_current
- Project directory path and filtered count

### 2. Preprocess Session to XML

```bash
erk exec preprocess-session <log-path> [OPTIONS]
```

**Options:**

- `--session-id`: Filter entries to specific session ID
- `--include-agents/--no-include-agents`: Include agent logs (default: True)
- `--no-filtering`: Disable filtering optimizations
- `--stdout`: Output to stdout instead of temp file

**Optimizations applied:**

- Empty/warmup session filtering
- Documentation deduplication (hash markers)
- Tool parameter truncation (>200 chars)
- Tool result pruning (first 30 lines, preserves errors)
- Log discovery operation filtering

### 3. Extract Plan from Session

```bash
erk exec extract-latest-plan [--session-id SESSION_ID]
```

Extracts most recent plan from session. Uses session-scoped lookup via slug field,
falls back to mtime-based lookup if no session-specific plan found.

### 4. Create GitHub Issue from Session

```bash
erk exec create-issue-from-session [--session-id SESSION_ID]
```

Extracts plan and creates GitHub issue with session content. Returns JSON with
issue_number and issue_url.

### 5. Render Session for GitHub

```bash
erk exec render-session-content --session-file <path> [--session-label LABEL] [--extraction-hints HINTS]
```

Renders session XML as GitHub comment blocks with automatic chunking for large content.

### 6. Extract Session from GitHub Issue

```bash
erk exec extract-session-from-issue <issue-number> [--output PATH] [--session-id ID]
```

Extracts and combines chunked session content from GitHub issue comments.

## Directory Structure

```
~/.claude/projects/
├── -Users-foo-code-myapp/           ← Encoded project path
│   ├── abc123-def456.jsonl          ← Main session log
│   ├── xyz789-ghi012.jsonl          ← Another session
│   ├── agent-17cfd3f4.jsonl         ← Agent subprocess log
│   └── agent-2a3b4c5d.jsonl         ← Another agent log
```

**Path encoding:** Prepend `-`, replace `/` and `.` with `-`

Example: `/Users/foo/code/myapp` → `-Users-foo-code-myapp`

## Session ID

Session IDs are passed explicitly to CLI commands via `--session-id` options. The typical flow:

1. Hook receives session context via stdin JSON from Claude Code
2. Hook outputs `📌 session: <id>` reminder to conversation
3. Agent extracts session ID from reminder text
4. Agent passes session ID as explicit CLI parameter

**Example:**

```bash
erk exec list-sessions --session-id abc123-def456
```

## Two-Stage Extraction Pipeline

The extraction system uses a two-stage pipeline:

### Stage 1: Mechanical Reduction (Deterministic)

- Drop file-history-snapshot entries
- Strip usage metadata
- Remove empty text blocks
- Compact whitespace (3+ newlines → 1)
- Deduplicate assistant messages with tool_use
- Output: Compressed XML

### Stage 2: Haiku Distillation (Optional, Semantic)

- Remove noise (log discovery, warmup content)
- Deduplicate semantically similar blocks
- Prune verbose outputs
- Preserves errors, stack traces, warnings
- Output: Semantically refined XML

## Session Selection Logic

The `auto_select_sessions()` function uses intelligent rules:

- **On trunk:** Use current session only
- **Current session trivial (<1KB) + substantial sessions exist:** Auto-select substantial
- **Current session substantial (>=1KB):** Use it alone
- **No substantial sessions:** Return current even if trivial

## Scratch Storage

Session-scoped files stored in `.erk/scratch/sessions/<session-id>/`:

```python
from erk_shared.scratch import get_scratch_dir, write_scratch_file

scratch_dir = get_scratch_dir(session_id)
file_path = write_scratch_file(content, session_id=session_id, suffix=".xml")
```

## Common Tasks

### Find What Happened in a Session

1. List sessions: `erk exec list-sessions`
2. Find by summary or time
3. Preprocess: `erk exec preprocess-session <file> --stdout | head -500`

### Debug Context Blowout

1. Run `/local:analyze-context`
2. Check token breakdown by category
3. Look for duplicate reads or large tool results

### Extract Plan for Implementation

```bash
erk exec extract-latest-plan --session-id <id>
```

### Create Issue from Session Plan

```bash
erk exec create-issue-from-session --session-id <id>
```

### Find Agent Subprocess Logs

```bash
PROJECT_DIR=$(erk find-project-dir | jq -r '.project_dir')
ls -lt "$PROJECT_DIR"/agent-*.jsonl | head -10
```

### Check for Errors in Agent

```bash
cat agent-<id>.jsonl | jq 'select(.message.is_error == true)'
```

## Resources

### references/

- `tools.md` - Complete CLI commands and jq analysis recipes
- `format.md` - JSONL format specification and entry types
- `extraction.md` - erk_shared extraction module API reference

Load references when users need detailed command syntax, format documentation, or
programmatic access to extraction capabilities.

## Code Dependencies

This skill documents capabilities that primarily live in:

- **CLI commands:** `packages/erk-cli/src/erk_cli/commands/`
- **Shared library:** `packages/erk-shared/src/erk_shared/extraction/`
- **GitHub metadata:** `packages/erk-shared/src/erk_shared/github/metadata.py`
- **Scratch storage:** `packages/erk-shared/src/erk_shared/scratch/`
