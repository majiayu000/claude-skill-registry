---
name: tasks-file
description: This skill should be used when managing the file-based task tracking system in the tasks directory. It provides workflows for creating tasks, managing status and dependencies, conducting triage, and integrating with slash commands and code review processes.
---

# File-Based Task Tracking Skill

## Overview

The `tasks` directory contains a file-based tracking system for managing code review feedback, technical debt, feature requests, and work items. Each task is a markdown file with YAML frontmatter and structured sections.

This skill should be used when:
- Creating new tasks from findings or feedback
- Managing task lifecycle (pending → ready → complete)
- Triaging pending items for approval
- Checking or managing dependencies
- Converting PR comments or code findings into tracked work
- Updating work logs during task execution

If you are unsure whether a repo uses file-based tasks or Beads, use the tasks-router skill first.

## File Naming Convention

Task files follow this naming pattern:

```
{issue_id}-{status}-{priority}-{description}.md
```

**Components:**
- **issue_id**: Sequential number (001, 002, 003...) - never reused
- **status**: `pending` (needs triage), `ready` (approved), `complete` (done)
- **priority**: `p1` (critical), `p2` (important), `p3` (nice-to-have)
- **description**: kebab-case, brief description

**Examples:**
```
001-pending-p1-mailer-test.md
002-ready-p1-fix-n-plus-1.md
005-complete-p2-refactor-csv.md
```

## File Structure

Each task is a markdown file with YAML frontmatter and structured sections. Use the template at [task-template.md](./assets/task-template.md) as a starting point when creating new tasks.

**Required sections:**
- **Problem Statement** - What is broken, missing, or needs improvement?
- **Findings** - Investigation results, root cause, key discoveries
- **Proposed Solutions** - Multiple options with pros/cons, effort, risk
- **Recommended Action** - Clear plan (filled during triage)
- **Acceptance Criteria** - Testable checklist items
- **Work Log** - Chronological record with date, actions, learnings

**Optional sections:**
- **Technical Details** - Affected files, related components, DB changes
- **Resources** - Links to errors, tests, PRs, documentation
- **Notes** - Additional context or decisions

**YAML frontmatter fields:**
```yaml
---
status: ready              # pending | ready | complete
priority: p1              # p1 | p2 | p3
issue_id: "002"
tags: [rails, performance, database]
dependencies: ["001"]     # Issue IDs this is blocked by
---
```

## Common Workflows

### Creating a New Task

**To create a new task from findings or feedback:**

1. Determine next issue ID: `ls tasks/ | grep -o '^[0-9]\+' | sort -n | tail -1`
2. Copy template: `cp assets/task-template.md tasks/{NEXT_ID}-pending-{priority}-{description}.md`
3. Edit and fill required sections:
   - Problem Statement
   - Findings (if from investigation)
   - Proposed Solutions (multiple options)
   - Acceptance Criteria
   - Add initial Work Log entry
4. Determine status: `pending` (needs triage) or `ready` (pre-approved)
5. Add relevant tags for filtering

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

### Triaging Pending Items

**To triage pending tasks:**

1. List pending items: `ls tasks/*-pending-*.md`
2. For each task:
   - Read Problem Statement and Findings
   - Review Proposed Solutions
   - Make decision: approve, defer, or modify priority
3. Update approved tasks:
   - Rename file: `mv {file}-pending-{pri}-{desc}.md {file}-ready-{pri}-{desc}.md`
   - Update frontmatter: `status: pending` → `status: ready`
   - Fill "Recommended Action" section with clear plan
   - Adjust priority if different from initial assessment
4. Deferred tasks stay in `pending` status

**Use slash command:** `/triage` for interactive approval workflow

### Managing Dependencies

**To track dependencies:**

```yaml
dependencies: ["002", "005"]  # This task blocked by issues 002 and 005
dependencies: []               # No blockers - can work immediately
```

**To check what blocks a task:**
```bash
grep "^dependencies:" tasks/003-*.md
```

**To find what a task blocks:**
```bash
grep -l 'dependencies:.*"002"' tasks/*.md
```

**To verify blockers are complete before starting:**
```bash
for dep in 001 002 003; do
  [ -f "tasks/${dep}-complete-*.md" ] || echo "Issue $dep not complete"
done
```

### Updating Work Logs

**When working on a task, always add a work log entry:**

```markdown
### YYYY-MM-DD - Session Title

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
```

Work logs serve as:
- Historical record of investigation
- Documentation of approaches attempted
- Knowledge sharing for team
- Context for future similar work

### Completing a Task

**To mark a task as complete:**

1. Verify all acceptance criteria checked off
2. Update Work Log with final session and results
3. Rename file: `mv {file}-ready-{pri}-{desc}.md {file}-complete-{pri}-{desc}.md`
4. Update frontmatter: `status: ready` → `status: complete`
5. Check for unblocked work: `grep -l 'dependencies:.*"002"' tasks/*-ready-*.md`
6. Commit with issue reference: `feat: resolve issue 002`

## Integration with Development Workflows

| Trigger | Flow | Tool |
|---------|------|------|
| Code review | `/workflows-review` → Findings → `/triage` → Tasks | Review agent + skill |
| PR comments | `/resolve_pr_parallel` → Individual fixes → Tasks | gh CLI + skill |
| Code TODOs | `/resolve_task_parallel` → Fixes + Complex tasks | Agent + skill |
| Planning | Brainstorm → Create task → Work → Complete | Skill |
| Feedback | Discussion → Create task → Triage → Work | Skill + slash |

## Quick Reference Commands

**Finding work:**
```bash
# List highest priority unblocked work
grep -l 'dependencies: \[\]' tasks/*-ready-p1-*.md

# List all pending items needing triage
ls tasks/*-pending-*.md

# Find next issue ID
ls tasks/ | grep -o '^[0-9]\+' | sort -n | tail -1 | awk '{printf "%03d", $1+1}'

# Count by status
for status in pending ready complete; do
  echo "$status: $(ls -1 tasks/*-$status-*.md 2>/dev/null | wc -l)"
done
```

**Dependency management:**
```bash
# What blocks this task?
grep "^dependencies:" tasks/003-*.md

# What does this task block?
grep -l 'dependencies:.*"002"' tasks/*.md
```

**Searching:**
```bash
# Search by tag
grep -l "tags:.*rails" tasks/*.md

# Search by priority
ls tasks/*-p1-*.md

# Full-text search
grep -r "payment" tasks/
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
