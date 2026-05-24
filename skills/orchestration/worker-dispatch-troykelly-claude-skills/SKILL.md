---
name: worker-dispatch
description: Use to spawn isolated worker processes for autonomous issue work. Uses Task tool with run_in_background for parallel execution and TaskOutput for monitoring. Pre-extracts context to minimize worker token usage.
allowed-tools:
  - Bash
  - Read
  - Task
  - TaskOutput
  - mcp__github__*
  - mcp__memory__*
model: opus
---

# Worker Dispatch

## Overview

Spawns and manages worker Claude agents using the **Task tool with `run_in_background: true`**. Workers run as parallel background agents monitored via **TaskOutput**.

**Core principle:** Workers are isolated, scoped, and expendable. State lives in GitHub, not in workers.

**Key optimization:** Pre-extract issue context BEFORE spawning. Workers receive focused context, not raw issues.

## Worktree Isolation (MANDATORY)

**CRITICAL:** Every worker MUST have its own git worktree. Workers NEVER operate in the main repository.

```
Main Repository (./)           ← Orchestrator only
    │
    └── Worktrees (isolated)
        ├── ../project-worker-123/    ← Worker for #123
        ├── ../project-worker-124/    ← Worker for #124
        └── ../project-worker-125/    ← Worker for #125
```

**Orchestrator responsibility:** Create worktree BEFORE spawning worker.
**Worker responsibility:** Verify isolation BEFORE any work (see `worker-protocol`).

This prevents file clobbering between parallel workers.

## Worker Types

| Type | Subagent | Purpose | When to Use |
|------|----------|---------|-------------|
| Implementation | `general-purpose` | Full feature work | Standard issue work |
| Research | `Explore` | Read-only investigation | Pre-implementation analysis, debugging |
| PR Resolution | `general-purpose` | Fix CI, merge PRs | Existing PR cleanup |

## Pre-Extraction (CRITICAL)

**Extract issue context BEFORE spawning.** Workers should not spend tokens re-reading issues.

```bash
extract_issue_context() {
  local issue=$1

  # Single API call to get everything
  ISSUE_JSON=$(gh issue view "$issue" --json title,body,labels,comments,assignees)

  TITLE=$(echo "$ISSUE_JSON" | jq -r '.title')
  BODY=$(echo "$ISSUE_JSON" | jq -r '.body')
  LABELS=$(echo "$ISSUE_JSON" | jq -r '[.labels[].name] | join(", ")')

  # Extract acceptance criteria if present
  ACCEPTANCE=$(echo "$BODY" | sed -n '/## Acceptance Criteria/,/^## /p' | head -20)
  [ -z "$ACCEPTANCE" ] && ACCEPTANCE=$(echo "$BODY" | sed -n '/- \[/p' | head -10)

  # Get latest handover if exists
  HANDOVER=$(echo "$ISSUE_JSON" | jq -r '
    [.comments[] | select(.body | contains("<!-- HANDOVER:START -->"))] | last | .body // ""
  ')

  # Get recent progress comments
  PROGRESS=$(echo "$ISSUE_JSON" | jq -r '
    [.comments[-3:][].body] | join("\n---\n")
  ' | head -50)
}
```

## Spawning Implementation Workers

### Step 1: Extract Context & Create Worktree

```bash
spawn_implementation_worker() {
  local issue=$1
  local attempt=${2:-1}

  # Pre-extract context
  extract_issue_context "$issue"

  worker_id="worker-$(date +%s)-$issue"
  issue_slug=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | cut -c1-40)
  branch="feature/$issue-$issue_slug"
  worktree_path="../$(basename $PWD)-worker-$issue"

  # Create worktree
  git fetch origin main
  git branch "$branch" origin/main 2>/dev/null || true
  git worktree add "$worktree_path" "$branch"
}
```

### Step 2: Register in GitHub

```bash
register_worker() {
  local issue=$1 worker_id=$2 worktree=$3

  gh issue comment "$issue" --body "<!-- WORKER:ASSIGNED -->
{\"worker_id\": \"$worker_id\", \"assigned_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}
<!-- /WORKER:ASSIGNED -->

**Worker Assigned:** \`$worker_id\` at $(date -u +%H:%M:%S)Z"

  update_project_status "$issue" "In Progress"
}
```

### Step 3: Construct Focused Prompt

**~50 lines with pre-extracted context:**

```bash
construct_worker_prompt() {
  local issue=$1 worker_id=$2 attempt=$3
  # Uses pre-extracted: TITLE, ACCEPTANCE, HANDOVER, PROGRESS

  cat <<PROMPT
Worker $worker_id | Issue #$issue | Attempt $attempt

## Task
$TITLE

## Requirements
$ACCEPTANCE

## Constraints
- Work ONLY on issue #$issue
- TDD: write tests first
- All tests must pass before PR
- Complete code review before PR (post artifact to issue)
- Max 100 turns - handover at 90+

## Exit Conditions
Return JSON when done:
\`\`\`json
{"status": "COMPLETED|BLOCKED|HANDOVER", "pr": null, "summary": "..."}
\`\`\`

| Status | Meaning |
|--------|---------|
| COMPLETED | PR created, tests pass |
| BLOCKED | Cannot proceed without external input |
| HANDOVER | Turn limit approaching, context posted |

## Progress Protocol
Post brief updates to issue. On handover, post full context with <!-- HANDOVER:START --> markers.

$([ -n "$HANDOVER" ] && echo "## Previous Handover
$HANDOVER")

$([ -n "$PROGRESS" ] && echo "## Recent Activity
$PROGRESS")

Begin implementation now.
PROMPT
}
```

### Step 4: Spawn Worker

```markdown
Task(
  description: "Issue #[ISSUE] worker",
  prompt: [FOCUSED_PROMPT],
  subagent_type: "general-purpose",
  run_in_background: true
)
```

**Returns:** `task_id` for monitoring.

## Spawning Research Workers

Use `Explore` subagent for read-only investigation before implementation:

```bash
construct_research_prompt() {
  local issue=$1 question=$2

  cat <<PROMPT
Research for issue #$issue: $TITLE

## Question
$question

## Scope
Investigate codebase to answer the question. Return structured findings.

## Output Format
\`\`\`json
{
  "findings": ["key finding 1", "key finding 2"],
  "relevant_files": ["path/to/file.ts"],
  "patterns": ["existing pattern to follow"],
  "concerns": ["potential issue to address"],
  "recommendation": "summary recommendation"
}
\`\`\`

Do NOT modify any files. Research only.
PROMPT
}
```

```markdown
Task(
  description: "Research for #[ISSUE]",
  prompt: [RESEARCH_PROMPT],
  subagent_type: "Explore",
  run_in_background: true
)
```

**Use cases:**
- Pre-implementation: "What patterns exist for similar features?"
- Debugging: "Where is this error originating?"
- Impact analysis: "What will this change affect?"

## Parallel Dispatch

Spawn multiple workers in ONE message for concurrent execution:

```markdown
## Dispatching 3 Workers

1. Extract context for each issue (sequential)
2. Invoke all Task tools in SAME message (parallel):

Task(description: "Issue #123 worker", prompt: [...], subagent_type: "general-purpose", run_in_background: true)
Task(description: "Issue #124 worker", prompt: [...], subagent_type: "general-purpose", run_in_background: true)
Task(description: "Issue #125 worker", prompt: [...], subagent_type: "general-purpose", run_in_background: true)

3. Store all returned task_ids
```

## Monitoring Workers

```markdown
TaskOutput(task_id: "[ID]", block: false, timeout: 1000)
```

| Result | Meaning | Action |
|--------|---------|--------|
| "Task is still running..." | Worker active | Continue monitoring |
| JSON with status | Worker complete | Parse result, update GitHub |
| Error | Worker failed | Check GitHub for context |

**Parse completion:**
```bash
RESULT=$(echo "$OUTPUT" | grep -oP '\{.*\}' | jq -r '.status')
PR=$(echo "$OUTPUT" | grep -oP '\{.*\}' | jq -r '.pr // empty')
```

## PR Workers

Resolve existing PRs (CI failures, missing reviews, merge):

```bash
construct_pr_worker_prompt() {
  local pr=$1 worker_id=$2

  cat <<PROMPT
PR Worker $worker_id | PR #$pr

## Mission
1. Check CI: \`gh pr checks $pr\`
2. If failing: investigate, fix, push
3. Verify review artifact exists on linked issue
4. If mergeable: \`gh pr merge $pr --squash --delete-branch\`

## Output
\`\`\`json
{"status": "MERGED|BLOCKED|HANDOVER", "summary": "..."}
\`\`\`

## Constraints
- Only fix CI-related issues
- Push to existing branch only
- Check for do-not-merge label

Begin with: \`gh pr checks $pr\`
PROMPT
}
```

## Worker Cleanup

On completion (detected via TaskOutput):

```bash
cleanup_worker() {
  local issue=$1 task_id=$2 result=$3

  gh issue comment "$issue" --body "<!-- WORKER:ASSIGNED -->
{\"assigned\": false, \"cleared_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}
<!-- /WORKER:ASSIGNED -->

**Worker Complete:** $result"

  case "$result" in
    COMPLETED) update_project_status "$issue" "In Review" ;;
    BLOCKED)   update_project_status "$issue" "Blocked" ;;
    HANDOVER)  ;; # Keep In Progress, spawn replacement
  esac
}
```

## Replacement Workers

When worker returns HANDOVER:

1. Handover context is in issue comments (already posted by worker)
2. Extract via: `extract_issue_context` (includes HANDOVER variable)
3. Spawn replacement with attempt+1
4. New worker receives full context automatically

## Checklist

**Before spawning:**
- [ ] Issue context pre-extracted
- [ ] Worktree created on feature branch
- [ ] Worker registered in GitHub
- [ ] Project board status: In Progress

**Prompt includes:**
- [ ] Pre-extracted title and acceptance criteria
- [ ] JSON output format requirement
- [ ] Previous handover (if any)
- [ ] Recent progress comments

**On completion:**
- [ ] JSON result parsed
- [ ] GitHub state updated
- [ ] Project board status updated
- [ ] Task_id removed from active list

## Integration

**Used by:** `autonomous-orchestration`, `claude-autonomous --pr`

**Uses:** `worker-protocol` (behavior contract), `worker-handover` (context format), `ci-monitoring` (PR workers)
