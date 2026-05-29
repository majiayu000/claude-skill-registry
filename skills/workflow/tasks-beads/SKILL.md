---
name: tasks-beads
description: This skill should be used when managing the Beads issue tracker via the `br` CLI. It provides workflows for creating tasks, triaging, managing dependencies, updating work logs, and completing issues using Beads instead of the filesystem.
---

# Beads Task Tracking Skill

## Overview

Beads is an agent-first issue tracker backed by `.beads/` (SQLite + JSONL). Use the `br` CLI to create, update, and complete tasks.

This skill should be used when:
- Creating new tasks from findings or feedback in Beads
- Managing issue lifecycle (open -> in_progress -> closed/deferred)
- Triaging pending items for priority and scope
- Checking or managing dependencies
- Converting PR comments or code findings into tracked Beads issues
- Updating work logs during task execution

If you are unsure whether a repo uses Beads or file-based tasks, use the tasks-router skill first.

## Key Concepts

- **IDs**: Issues have IDs (no filenames).
- **Statuses**: `open`, `in_progress`, `deferred`, `closed`.
- **Priority**: `P0`-`P4` or `0`-`4` (0 = critical, 4 = backlog).
- **Types**: `task`, `bug`, `feature`, `epic`, `question`, `docs`.
- **Storage**: `.beads/` contains the database and JSONL export.

## Type Mapping

Choose `--type` based on category:

- Bug -> `bug`
- Feature -> `feature`
- Docs / Documentation -> `docs`
- Question -> `question`
- Epic -> `epic`
- Security / Performance / Architecture / Quality / Refactor / Unknown -> `task`

## Field Mapping (Tasks-File -> Beads)

Use Beads fields optimally to preserve structure and enable filtering:

| tasks-file Section | Beads Field | Usage |
|-------------------|-------------|-------|
| Title | `title` | Brief summary |
| Problem Statement | `description` | What's broken & why it matters |
| Findings | `notes` | Investigation results, root cause |
| Proposed Solutions | `design` | Options with pros/cons/effort/risk |
| Technical Details | `design` | Affected files, components, DB changes |
| Recommended Action | `notes` | Approved plan (add after triage) |
| Resources | `external_ref` + `notes` | Primary ref (PR#) → external_ref |
| Acceptance Criteria | `acceptance_criteria` | Testable checklist |
| Work Log | `comments` | One comment per session |
| Additional Notes | `notes` | Context, decisions, blockers |
| Effort Estimate | `estimated_minutes` | From chosen solution option |
| Tags | `labels` | `--add-label` for filtering |
| Dependencies | `dependencies` | `br dep add` |
| Priority | `priority` | p1→P1, p2→P2, p3→P3 |

**Field purposes:**
- `description` — The problem (what & why)
- `design` — The solution (how) — technical approach, options, architecture
- `notes` — Context (findings, resources, decisions)
- `acceptance_criteria` — Definition of done
- `comments` — Work log (append-only history)

Use the template at [task-template.md](./assets/task-template.md) for section structure.

## Common Workflows

### Creating a New Task

**To create a new task from findings or feedback:**

1. Create the issue with core metadata:
   ```bash
   br create --title="Short summary" --type=bug --priority=2 \
     --description="Problem statement - what's broken and why it matters" --json
   ```

2. Add technical design (solutions, architecture, affected files):
   ```bash
   br update <id> --design="## Proposed Solutions

### Option 1: [Name]
**Approach:** ...
**Pros:** ...
**Cons:** ...
**Effort:** 2-3 hours
**Risk:** Low

## Technical Details
**Affected files:**
- path/to/file.rb:42
**Related components:**
- ComponentA, ComponentB" --json
   ```

3. Add findings and context:
   ```bash
   br update <id> --notes="## Findings
- Root cause: ...
- Investigation showed: ...

## Resources
- PR: #1287
- Docs: [link]" --json
   ```

4. Add acceptance criteria:
   ```bash
   br update <id> --acceptance-criteria="- [ ] Tests pass
- [ ] Code reviewed
- [ ] Performance acceptable" --json
   ```

5. Set effort estimate and labels:
   ```bash
   br update <id> --estimate=120 --add-label "performance" --add-label "db" --json
   ```

6. Link external references (optional):
   ```bash
   br update <id> --external-ref="PR#1287" --json
   ```

**When to create a task:**
- Requires more than 15-20 minutes of work
- Needs research, planning, or multiple approaches considered
- Has dependencies on other work
- Requires manager approval or prioritization
- Part of larger feature or refactor
- Technical debt needing documentation

**When to act immediately instead:**
- Issue is trivial (< 15 minutes)
- Complete context available now
- No planning needed
- User explicitly requests immediate action
- Simple bug fix with obvious solution

### Triaging Open Items

**To triage open tasks:**

1. List open items:
   ```bash
   br list --status=open --sort=priority --json
   ```
2. For each issue:
   - Read description and notes: `br show <id> --json`
   - Decide: reprioritize, clarify scope, or defer
3. Update status/priority as needed:
   ```bash
   br update <id> --priority=1 --json
   br update <id> --status=deferred --defer="2026-03-01" --json
   ```

**Ready work (unblocked):**
```bash
br ready --json
```

### Managing Dependencies

**To add dependencies:**
```bash
br dep add <issue> <depends-on> --json
```

**To list dependencies:**
```bash
br dep list <issue> --json
```

**To find dependency cycles:**
```bash
br dep cycles --json
```

**To see a dependency tree:**
```bash
br dep tree <issue> --json
```

### Starting Work on a Task

**Before working on a task, claim it to set status and assignee atomically:**

```bash
br update <id> --claim --json
```

This sets `status=in_progress` and `assignee=<actor>` in one step.

### Updating Work Logs

**When working on a task, add a work log entry as a comment:**

```bash
cat <<'EONOTE' > /tmp/beads-comment.md
### 2026-02-03 - Session Title

**By:** Claude Code / Developer Name

**Actions:**
- Specific changes made (include file:line references)
- Commands executed
- Tests run
- Results of investigation

**Learnings:**
- What worked / what didn't
- Patterns discovered
- Key insights for future work
EONOTE

br comments add <id> -f /tmp/beads-comment.md --json
```

Work logs serve as:
- Historical record of investigation
- Documentation of approaches attempted
- Knowledge sharing for team
- Context for future similar work

### Completing a Task

**To mark a task as complete:**

1. Verify acceptance criteria are met
2. Add a final work log entry
3. Close the issue:
   ```bash
   br close <id> --reason="Completed" --json
   ```
4. Check for unblocked work:
   ```bash
   br ready --json
   ```

## Integration with Development Workflows

| Trigger | Flow | Tool |
|---------|------|------|
| Code review | Findings -> Create issue -> Triage -> Work | Review agent + Beads |
| PR comments | Resolve -> Create issue for remaining work | gh CLI + Beads |
| Code TODOs | Fix easy items -> Create issue for complex items | Agent + Beads |
| Planning | Brainstorm -> Create issue -> Work -> Close | Beads |
| Feedback | Discussion -> Create issue -> Triage -> Work | Beads |

## Quick Reference Commands

**Finding work:**
```bash
# Ready (unblocked) work
br ready --json

# Open high-priority work
br list --status=open --priority-max=1 --json

# Count by status
br count --group-by status --json
```

**Searching:**
```bash
# Full-text search
br search "payment failure" --json

# By label
br list --label "performance" --json
```

**Data hygiene:**
```bash
# Show workspace location
br where --json

# Sync DB <-> JSONL
br sync --status --json
br sync --flush-only --json
```

## Key Distinctions

**Tasks-file system (this skill):**
- Markdown files in `tasks/` directory
- Standalone files with YAML frontmatter
- Human-readable, git-friendly
- Use when repo has no `.beads/` directory

**Tasks-beads system:**
- SQLite + JSONL in `.beads/` directory
- Managed via `br` CLI
- Structured fields, richer queries
- Use when repo has `.beads/` directory
- See tasks-beads skill for details

**Tasks-router skill:**
- Routes to tasks-file or tasks-beads based on repo state
- Use when unsure which system applies

**TodoWrite tool:**
- In-memory task tracking during agent sessions
- Temporary tracking for single conversation
- Not persisted to disk
- Different from both persistent systems above
