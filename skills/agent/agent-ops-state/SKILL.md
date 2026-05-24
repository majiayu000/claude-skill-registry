---
name: agent-ops-state
description: "Maintain .agent state files. Use at session start, after meaningful steps, and before concluding: read/update constitution/memory/focus/issues/baseline consistently."
category: core
invokes: [agent-ops-git]
invoked_by: [all-skills]
state_files:
  read: [constitution.md, memory.md, focus.md, issues/*.md, baseline.md]
  write: [focus.md, issues/*.md, memory.md]
---

# AgentOps State Discipline

**Works with or without `aoc` CLI installed.** State management uses direct file operations by default.

## State File Operations (Default)

All state files are managed via direct file operations:

| File | Operations |
|------|-----------|
| `.agent/constitution.md` | Read/write directly |
| `.agent/focus.md` | Read/write directly |
| `.agent/memory.md` | Read/write directly |
| `.agent/baseline.md` | Read/write directly |
| `.agent/issues/{priority}.md` | Read/append/edit directly |

### Issue Management (File-Based)

| Operation | How to Do It |
|-----------|--------------|
| List issues by priority | Read `.agent/issues/{priority}.md` directly |
| Show issue details | Search for issue ID in priority files |
| Create issue | Append to appropriate `.agent/issues/{priority}.md` file |
| Update issue status | Edit `status:` field directly in file |
| Close issue | Set `status: done` + move to `history.md` |
| Get summary | Count issues across priority files |

### Git Status

```bash
# Check current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain

# Get last commit hash
git rev-parse --short HEAD
```

## CLI Integration (when aoc is available)

When `aoc` CLI is detected in `.agent/tools.json`, these commands provide convenience shortcuts:

| Operation | CLI Command |
|-----------|-------------|
| List issues by priority | `aoc issues list --priority critical` |
| Show issue details | `aoc issues show <ID>` |
| Create issue | `aoc issues create --type BUG --title "..."` |
| Update issue status | `aoc issues update <ID> --status in-progress` |
| Close issue | `aoc issues close <ID>` |
| Get summary | `aoc issues summary` |

**Note:** CLI is optional — all operations can be performed via direct file editing.

## When to Use
- At the start of a session/response
- After any meaningful step (analysis/plan decision/implementation/test run)
- When adding/updating issues
- Before concluding a response

## Session Start

At session start:
1. **Check for staleness**: Delegate to `agent-ops-git` stale detection
2. **Read state files** in order (see below)
3. **Validate issue dependencies** before starting work

## Required Reads (in this order)
1) `.agent/constitution.md`
2) `.agent/focus.md`
3) `.agent/memory.md`
4) `.agent/issues/index.md` (compact issue summary — read this FIRST for issue overview)
5) `.agent/issues/critical.md` and `.agent/issues/critical-*.md` (only if working on critical)
6) `.agent/issues/high.md` and `.agent/issues/high-*.md` (only if working on high)
7) `.agent/issues/medium.md` and `.agent/issues/medium-*.md` (only if needed)
8) `.agent/issues/low.md` and `.agent/issues/low-*.md` (only if needed)
9) `.agent/baseline.md` (if present)

**Context Optimization:** Read `index.md` first to understand the issue landscape. Only read full priority files when actively working on an issue from that priority level.

**Note on split files:** Issue files may be split when they exceed 100K. Always scan for `{priority}-*.md` files (e.g., `backlog-1.md`, `history-2.md`). Oldest issues are in numbered files, newest in the main file.

## Required Updates

### `.agent/focus.md`
Must always contain:
- Session info (last_updated timestamp, branch, last_commit)
- Just did (what changed since last update)
- Doing now (current objective + issue ID if working on one)
- Next (single best next step + prerequisites/unknowns)

### `.agent/issues/{priority}.md`
- Issues stored by priority: critical.md, high.md, medium.md, low.md
- Only use the repo issue format (see template)
- Create issues for follow-ups, blockers, open questions, approvals needed
- Validate `depends_on` before starting an issue

### `.agent/memory.md`
- Only store durable learnings (workflow rules, stable conventions)
- Do not duplicate constitution content

## Dependency Validation

Before starting an issue:
1. Read issue's `depends_on` field
2. Search all priority files for dependency issues
3. Check each dependency's status
4. If any dependency is not `done`: mark issue as `blocked`, note which
5. Only proceed if all dependencies satisfied

## Templates
- [focus template](./templates/focus.template.md)
- [memory template](./templates/memory.template.md)
- [issues template](./templates/issues.template.md)
