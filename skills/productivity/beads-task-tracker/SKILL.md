---
name: beads-task-tracker
description: Use Beads (bd tool) for dependency-aware task tracking and long-horizon planning in coding projects. This skill should be used when working on complex multi-step projects that span multiple agent sessions, when discovering new work during implementation, or when explicit task dependency management would improve workflow organization and prevent context loss between sessions.
---

# Beads Task Tracker

## Overview

Beads is a git-versioned, dependency-aware issue tracker designed specifically for AI coding agents. It solves the "amnesia problem" where agents lose context between sessions by providing a persistent, queryable task database that agents can use to orient themselves, find ready work, and track dependencies across long-horizon projects.

Use Beads when:
- Working on projects with multiple interconnected tasks
- Tasks span multiple agent sessions (>10 minutes)
- Need to track what work is blocked vs. ready
- Discovering new work during implementation that should be captured
- Multiple agents or machines are working on the same codebase
- Want to avoid the "markdown plan swamp" where plans become stale and disorganized

## Installation Check

Before using Beads, verify the `bd` command is installed:

```bash
bd version
```

If not installed, install via:

```bash
curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh | bash
```

**Post-installation PATH setup:**

After installation, if `bd` is not found in your PATH, add the Go bin directory to your shell profile:

For zsh (most macOS systems), add to `~/.zshrc`:
```bash
export PATH="$PATH:$HOME/go/bin"
```

For bash, add to `~/.bashrc` or `~/.bash_profile`:
```bash
export PATH="$PATH:$HOME/go/bin"
```

Then reload your shell:
```bash
source ~/.zshrc  # or source ~/.bashrc
```

Alternatively, you can use the full path `/Users/[username]/go/bin/bd` until PATH is configured.

## Workflow Overview

### 1. Project Initialization

Initialize Beads in a project directory (only needed once per project):

```bash
bd init
```

This creates a `.beads/` directory with:
- `issues.jsonl` - Git-versioned source of truth
- `*.db` - Local SQLite cache (gitignored)

### 2. Creating Work

Create issues when starting new work or discovering tasks during implementation:

**Basic creation:**
```bash
bd create "Task title" -d "Description" -p 1 -t task --json
```

**Issue types:**
- `task` - Standard work item (default)
- `feature` - New functionality
- `bug` - Defect to fix
- `epic` - Large body of work (parent to multiple tasks)
- `chore` - Maintenance work

**Priority levels (0-4):**
- `0` - Critical/blocking
- `1` - High priority
- `2` - Medium priority (default)
- `3` - Low priority
- `4` - Nice to have

**Creating from markdown file:**
```bash
bd create -f plan.md --json
```

Format: `## Issue Title` creates new issue, with optional sections `### Priority`, `### Type`, `### Description`, `### Dependencies`

**Add labels for organization:**
```bash
bd create "Add auth" -l "backend,security,p1" --json
```

### 3. Managing Dependencies

Link related work to establish ordering and track blockers:

**Add dependency:**
```bash
# Format: bd dep add <dependent> <blocker>
bd dep add bd-5 bd-3  # bd-5 depends on bd-3 completing first
```

**Dependency types:**

- `blocks` (default) - Hard blocker; dependent cannot start until blocker closes
- `parent-child` - Hierarchical relationship (child depends on parent)
  ```bash
  bd dep add bd-task bd-epic --type parent-child
  ```
- `discovered-from` - Issue found during work on another issue
  ```bash
  bd dep add bd-new bd-current --type discovered-from
  ```
- `related` - Soft connection; issues are related but not blocking

**Visualize dependencies:**
```bash
bd dep tree bd-42 --json
```

**Detect cycles:**
```bash
bd dep cycles --json
```

Cycles break ready work detection and must be resolved.

### 4. Finding Ready Work

Query for actionable work with no open blockers:

```bash
# All ready work
bd ready --json

# Filter by priority
bd ready --priority 1 --json

# Filter by labels
bd ready --label backend --json

# Limit results
bd ready --limit 5 --json
```

#### Finding Recent/Latest Tasks

**IMPORTANT:** When starting a session, always check for the **latest/highest-numbered tasks first**, as these typically represent the most recent work and current priorities.

**View recent tasks sorted by ID (descending):**

```bash
# List all open tasks, sorted by ID number (highest/newest first)
bd list --status open --json | jq -r '.[] | .id' | sort -t'-' -k3 -n -r | head -20

# Show full details of highest-numbered tasks
bd list --status open --json | jq 'sort_by(.id | sub(".*-"; "") | tonumber) | reverse | .[0:10]'

# Find tasks in a specific number range (e.g., 120-150)
bd list --json | jq '[.[] | select(.id | test("Twilio-Aldea-1[2-5][0-9]"))] | sort_by(.id | sub(".*-"; "") | tonumber) | reverse | .[] | {id, title, status, priority}'
```

**Example workflow at session start:**

```bash
# 1. First, check what the highest task numbers are
HIGHEST=$(bd list --json | jq -r '.[].id' | grep -oE '[0-9]+$' | sort -n | tail -1)
echo "Highest task number: $HIGHEST"

# 2. View tasks in the recent range (e.g., last 30 tasks)
RANGE_START=$((HIGHEST - 30))
bd list --json | jq --arg start "$RANGE_START" '[.[] | select(.id | test(".*-([0-9]+)$") and (.id | match(".*-([0-9]+)$").captures[0].string | tonumber) >= ($start | tonumber))] | sort_by(.id | sub(".*-"; "") | tonumber) | reverse'

# 3. Find ready work among recent tasks
bd ready --json | jq -r '.[] | .id' | sort -t'-' -k3 -n -r | head -10
```

**Why check recent tasks first:**

- Most recent work is usually the current focus
- Recent tasks often have the freshest context
- Prevents overlooking newly-created high-priority work
- Helps identify what was worked on most recently

**At session start, always:**

1. Check the highest task numbers to understand the current work range
2. List recent tasks (highest 20-30 IDs) to see current focus areas
3. Run `bd ready --json` to find unblocked work, prioritizing recent tasks
4. Choose highest-priority ready issue (preferring recent tasks when priorities are equal)
5. Update status to `in_progress` before starting work

### 5. Working and Updating

Update issue status as work progresses:

**Start work:**
```bash
bd update bd-42 --status in_progress --json
```

**Valid statuses:**
- `open` - Not started
- `in_progress` - Currently being worked on
- `closed` - Completed

**Update other fields:**
```bash
bd update bd-42 --priority 0 --json
bd update bd-42 --assignee alice --json
```

**Close completed work:**
```bash
bd close bd-42 --reason "Implementation complete, tests passing" --json
```

### 6. Discovery During Work

When discovering new work during implementation:

```bash
# 1. Create the discovered issue
NEW_ID=$(bd create "Fix discovered bug in auth" -t bug -p 1 --json | jq -r '.id')

# 2. Link back to parent work
bd dep add $NEW_ID bd-current --type discovered-from --json

# 3. Decide: handle now or defer?
# If blocking current work: switch to new issue
# If not blocking: continue current work, new issue will show in bd ready
```

### 7. Querying and Inspection

**List issues with filters:**
```bash
bd list --status open --json
bd list --priority 1 --json
bd list --label backend,urgent --json  # AND: must have ALL
bd list --label-any frontend,backend --json  # OR: at least one
```

**Show full issue details:**
```bash
bd show bd-42 --json
```

**View blocked issues:**
```bash
bd blocked --json
```

**Project statistics:**
```bash
bd stats --json
```

## JSON Output Parsing

Always use `--json` flag for programmatic access. Parse with `jq`:

```bash
# Get first ready issue
ISSUE=$(bd ready --json | jq -r '.[0]')
ISSUE_ID=$(echo "$ISSUE" | jq -r '.id')
ISSUE_TITLE=$(echo "$ISSUE" | jq -r '.title')

# Check if any ready work exists
READY_COUNT=$(bd ready --json | jq 'length')
if [ "$READY_COUNT" -eq 0 ]; then
  echo "No ready work. Check blocked issues:"
  bd blocked --json
fi

# Get highest task number and list recent tasks
HIGHEST=$(bd list --json | jq -r 'max_by(.id | sub(".*-"; "") | tonumber) | .id | sub(".*-"; "")')
echo "Highest task: #$HIGHEST"
bd list --json | jq --arg num "$HIGHEST" '[.[] | select((.id | sub(".*-"; "") | tonumber) >= (($num | tonumber) - 20))] | sort_by(.id | sub(".*-"; "") | tonumber) | reverse | .[] | {id, title, status, priority}'
```

## Best Practices

**DO:**
- Initialize Beads at project start (`bd init`)
- Create issues for discovered work instead of informal notes
- Use dependencies to model task relationships
- Query `bd ready` at session start to orient yourself
- Close issues with descriptive reasons
- Use labels to categorize work (e.g., `backend`, `frontend`, `urgent`)
- Commit `.beads/issues.jsonl` to git (auto-exported after changes)

**DON'T:**
- Create circular dependencies (use `bd dep cycles` to detect)
- Skip updating status (stale statuses confuse ready work detection)
- Forget to link discovered work back to parent issues
- Use markdown files for task tracking when Beads is available
- Ignore blocked issues indefinitely (reassess dependencies)

## Multi-Session Workflow Pattern

**Session 1 - Starting fresh:**
```bash
# 1. Check for ready work
bd ready --json

# 2. If no ready work, check what's blocked
bd blocked --json

# 3. Start working on highest-priority ready issue
bd update bd-5 --status in_progress --json

# 4. During work, discover new issue
bd create "Fix validation bug" -t bug -p 0 --json
bd dep add bd-new bd-5 --type discovered-from --json

# 5. Complete original work
bd close bd-5 --reason "Feature implemented" --json
```

**Session 2 - Agent resumes (different session, possibly different day):**
```bash
# 1. Check ready work (newly created bd-new is now ready)
bd ready --json

# 2. See discovered issue from previous session
# 3. Continue work seamlessly without context loss
bd update bd-new --status in_progress --json
```

## Quick Reference

See `references/quick-reference.md` for a comprehensive command cheat sheet.

For workflow patterns and advanced usage, see `references/workflow-patterns.md`.

## Built-in Help

Beads includes an interactive quickstart guide:

```bash
bd quickstart
```

Run this to see comprehensive examples and workflows.

## Integration with Project Documentation

Add to `AGENTS.md` or `CLAUDE.md`:

```markdown
## Task Tracking with Beads

We track implementation work using Beads (`bd`), a dependency-aware issue tracker. Use `bd ready --json` to see unblocked work, `bd create` to add tasks, and `bd update <id> --status in_progress` to claim work. Run `bd quickstart` for full documentation.
```

## Resources

This skill includes reference documentation to support effective Beads usage:

### references/

- `quick-reference.md` - Command cheat sheet organized by category
- `workflow-patterns.md` - Common patterns and best practices for agent workflows
