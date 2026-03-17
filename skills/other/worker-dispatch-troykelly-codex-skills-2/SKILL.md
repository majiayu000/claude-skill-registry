---
name: worker-dispatch
description: Use to spawn isolated worker processes for autonomous issue work. Creates git worktrees, constructs worker prompts, and handles worker lifecycle.
---

# Worker Dispatch

## Overview

Spawns and manages worker Codex processes in isolated git worktrees. Workers are disposable - if they fail, spawn another.

**Core principle:** Workers are isolated, scoped, and expendable. State lives in GitHub, not in workers.

**Announce at start:** "I'm using worker-dispatch to spawn a worker for issue #[N]."

## State Management

**CRITICAL:** Worker state is stored in GitHub. NO local state files for tracking.

| State | Location | Purpose |
|-------|----------|---------|
| Worker assignment | Issue comment | Who is working on what |
| Worker status | Project Board | In Progress, Done, etc. |
| Process logs | Local (ephemeral) | Debugging only |
| Process PIDs | Local (ephemeral) | Process management only |

Local files (logs, PIDs) are ephemeral - they exist only for the current orchestration session. All persistent state is in GitHub.

## Worker Architecture

```
Main Repository (./)
│
└── Worktrees (parallel directories)
    │
    ├── ../project-worker-123/    ← Worker for issue #123
    │   └── (full repo copy on feature/123-* branch)
    │
    ├── ../project-worker-124/    ← Worker for issue #124
    │   └── (full repo copy on feature/124-* branch)
    │
    └── ../project-worker-125/    ← Worker for issue #125
        └── (full repo copy on feature/125-* branch)
```

## Spawning a Worker

### Step 1: Create Worktree

```bash
spawn_worker() {
  issue=$1
  context_file=$2  # Optional: handover context

  worker_id="worker-$(date +%s)-$issue"

  issue_title=$(gh issue view "$issue" --json title --jq '.title' | \
    tr '[:upper:]' '[:lower:]' | \
    sed 's/[^a-z0-9]/-/g' | \
    cut -c1-40)

  branch="feature/$issue-$issue_title"
  worktree_path="../$(basename $PWD)-worker-$issue"

  git fetch origin main
  git branch "$branch" origin/main 2>/dev/null || true
  git worktree add "$worktree_path" "$branch"

  echo "Created worktree: $worktree_path on branch $branch"
}
```

### Step 2: Register Worker in GitHub

Post worker assignment to the issue as a structured comment:

```bash
register_worker() {
  worker_id=$1
  issue=$2
  worktree=$3

  # Post assignment comment with structured marker
  gh issue comment "$issue" --body "<!-- WORKER:ASSIGNED -->
\`\`\`json
{
  \"assigned\": true,
  \"worker_id\": \"$worker_id\",
  \"assigned_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
  \"worktree\": \"$worktree\"
}
\`\`\`
<!-- /WORKER:ASSIGNED -->

**Worker Assigned**
- **Worker ID:** \`$worker_id\`
- **Started:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
- **Worktree:** \`$worktree\`

---
*Orchestrator: $ORCHESTRATION_ID*"

  # Update project board status
  update_project_status "$issue" "In Progress"
}
```

### Step 3: Construct Worker Prompt

```bash
construct_worker_prompt() {
  issue=$1
  worker_id=$2
  context_file=$3
  attempt=$4
  research_context=$5

  cat <<PROMPT
You are a worker agent. Your ONLY task is to complete GitHub issue #$issue.

## Worker Identity
- **Worker ID:** $worker_id
- **Issue:** #$issue
- **Attempt:** $attempt
- **Orchestration:** $ORCHESTRATION_ID

## Your Mission
Complete issue #$issue by following the issue-driven-development workflow:
1. Read and understand the issue completely
2. Create/verify you're on the correct branch
3. Implement the solution with TDD
4. Run all tests
5. Create a PR when complete
6. Update issue with progress comments throughout

## Constraints
- Work ONLY on issue #$issue - no other issues
- Do NOT modify unrelated code
- Do NOT start other work
- Follow all project skills (strict-typing, ipv6-first, etc.)
- Maximum 100 turns - if approaching limit, prepare handover

## Exit Conditions
Exit when ANY of these occur:
1. **PR Created** - Your work is complete
2. **Blocked** - You cannot proceed without external input
3. **Turns Exhausted** - Approaching 100 turns, handover needed
4. **Failed** - Tests fail after good-faith effort (triggers research)

## Progress Reporting
Update the issue with comments as you work.

## On Completion
Post completion comment to the issue.

## On Handover Needed
Post handover context to the issue comment (NOT local file).

$(if [ -n "$context_file" ] && [ -f "$context_file" ]; then
  echo "## Context from Previous Worker"
  cat "$context_file"
fi)

$(if [ -n "$research_context" ]; then
  echo "## Research Context (Previous Failures)"
  echo "$research_context"
fi)

## Begin
Start by reading issue #$issue to understand the requirements.
PROMPT
}
```

### Step 4: Spawn Process

```bash
spawn_worker_process() {
  issue=$1
  worker_id=$2
  worktree_path=$3
  prompt=$4

  # Create local ephemeral directories
  mkdir -p ".codex/logs" ".codex/pids"
  log_file=".codex/logs/$worker_id.log"
  pid_file=".codex/pids/$worker_id.pid"

  (
    cd "$worktree_path"
    codex exec --dangerously-bypass-approvals-and-sandbox --json -C "$worktree_path" "$prompt" 2>&1
  ) > "$log_file" &

  worker_pid=$!
  echo "$worker_pid" > "$pid_file"

  echo "Spawned worker $worker_id (PID: $worker_pid) for issue #$issue"
}
```

### Complete Spawn Function

```bash
spawn_worker() {
  issue=$1
  context_file=${2:-""}
  attempt=${3:-1}
  research_context=${4:-""}

  worker_id="worker-$(date +%s)-$issue"
  worktree_path=$(create_worktree "$issue" "$worker_id")
  prompt=$(construct_worker_prompt "$issue" "$worker_id" "$context_file" "$attempt" "$research_context")

  # Register in GitHub BEFORE spawning
  register_worker "$worker_id" "$issue" "$worktree_path"

  # Spawn process
  spawn_worker_process "$issue" "$worker_id" "$worktree_path" "$prompt"

  log_activity "worker_spawned" "$worker_id" "$issue"
}
```

## Tool Scoping

### Standard Worker (Full Implementation)

```bash
--allowedTools "Bash,Read,Edit,Write,Grep,Glob,mcp__git__*,mcp__github__*,mcp__memory__*,WebFetch,WebSearch"
```

### Research Worker (Read-Only)

```bash
--allowedTools "Read,Grep,Glob,WebFetch,WebSearch,mcp__memory__*,mcp__github__get_issue,mcp__github__get_pull_request"
```

### Review Worker (No Edits)

```bash
--allowedTools "Read,Grep,Glob,Bash(pnpm test:*),Bash(pnpm lint:*)"
```

## Checking Worker Status

Check both GitHub and local PID:

```bash
check_worker_status() {
  worker_id=$1
  issue=$2

  pid_file=".codex/pids/$worker_id.pid"

  if [ ! -f "$pid_file" ]; then
    echo "unknown"
    return
  fi

  pid=$(cat "$pid_file")

  if ! kill -0 "$pid" 2>/dev/null; then
    # Process exited - check GitHub for status
    pr_exists=$(gh pr list --head "feature/$issue-*" --json number --jq 'length')

    if [ "$pr_exists" -gt 0 ]; then
      echo "completed"
    else
      # Check issue comments for status
      log_file=".codex/logs/$worker_id.log"
      if [ -f "$log_file" ]; then
        if grep -q 'handover' "$log_file"; then
          echo "handover_needed"
        elif grep -q 'blocked' "$log_file"; then
          echo "blocked"
        else
          echo "failed"
        fi
      else
        echo "unknown"
      fi
    fi
  else
    echo "running"
  fi
}
```

## Worker Cleanup

```bash
cleanup_worker() {
  worker_id=$1
  issue=$2
  keep_worktree=${3:-false}

  worktree="../$(basename $PWD)-worker-$issue"

  # Remove worktree (unless keeping for inspection)
  if [ "$keep_worktree" = "false" ] && [ -d "$worktree" ]; then
    git worktree remove "$worktree" --force 2>/dev/null || true
    git worktree prune
  fi

  # Clean up local ephemeral files
  rm -f ".codex/pids/$worker_id.pid"

  # Post cleanup comment to issue
  gh issue comment "$issue" --body "<!-- WORKER:ASSIGNED -->
\`\`\`json
{\"assigned\": false, \"cleared_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}
\`\`\`
<!-- /WORKER:ASSIGNED -->

**Worker Cleaned Up**
- **Worker ID:** \`$worker_id\`
- **Cleared:** $(date -u +%Y-%m-%dT%H:%M:%SZ)

---
*Orchestrator: $ORCHESTRATION_ID*"

  log_activity "worker_cleaned" "$worker_id" "$issue"
}
```

## Replacement Worker (After Handover)

```bash
spawn_replacement_worker() {
  old_worker_id=$1
  issue=$2
  worktree=$3

  # Get handover context from issue comments
  handover_context=$(gh api "/repos/$OWNER/$REPO/issues/$issue/comments" \
    --jq '[.[] | select(.body | contains("<!-- HANDOVER:START -->"))] | last | .body' 2>/dev/null || echo "")

  # Cleanup old worker but KEEP worktree
  cleanup_worker "$old_worker_id" "$issue" true

  # Spawn replacement with handover context
  new_worker_id="worker-$(date +%s)-$issue"
  attempt=$(($(get_attempt_count "$issue") + 1))

  prompt=$(construct_worker_prompt "$issue" "$new_worker_id" "" "$attempt" "$handover_context")
  register_worker "$new_worker_id" "$issue" "$worktree"
  spawn_worker_process "$issue" "$new_worker_id" "$worktree" "$prompt"

  log_activity "worker_replacement" "$new_worker_id" "$issue" "$old_worker_id"
}
```

## Parallel Dispatch

```bash
dispatch_available_slots() {
  max_workers=5

  # Count current workers from project board (In Progress status)
  current=$(gh project item-list "$GITHUB_PROJECT_NUM" --owner "$GH_PROJECT_OWNER" \
    --format json | jq '[.items[] | select(.status.name == "In Progress")] | length')

  available=$((max_workers - current))

  if [ "$available" -le 0 ]; then
    echo "No worker slots available ($current/$max_workers active)"
    return
  fi

  echo "Dispatching up to $available workers..."

  for i in $(seq 1 $available); do
    next_issue=$(get_next_pending_issue)

    if [ -z "$next_issue" ]; then
      echo "No more pending issues"
      break
    fi

    spawn_worker "$next_issue"
  done
}
```

## Checklist

When spawning a worker:

- [ ] Worktree created successfully
- [ ] Branch created/checked out
- [ ] Worker registered in GitHub (issue comment)
- [ ] Project board status updated to In Progress
- [ ] Worker prompt constructed with all context
- [ ] Appropriate tool scoping applied
- [ ] Process spawned in background
- [ ] Activity logged

When cleaning up:

- [ ] Worker process terminated (or already exited)
- [ ] Worktree removed (unless keeping for inspection)
- [ ] Cleanup comment posted to issue
- [ ] Activity logged

## Integration

This skill is used by:
- `autonomous-orchestration` - Main orchestration loop

This skill uses:
- `worker-protocol` - Behavior injected into prompts
- `worker-handover` - Handover context format
