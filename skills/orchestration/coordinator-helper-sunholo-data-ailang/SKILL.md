---
name: Coordinator Helper
description: Manage coordinator daemon tasks, approve/reject work, monitor autonomous agents. Use when user asks to delegate tasks, check task status, review agent work, manage the coordinator, or use GitHub-driven approval workflow.
---

# Coordinator Helper

Manage the coordinator daemon for autonomous task delegation, approval workflows, and monitoring agent work.

## Quick Start

**Most common usage:**
```bash
# User says: "Delegate this bug fix to an agent"
# This skill will:
# 1. Check if coordinator daemon is running
# 2. Send the task via ailang messages
# 3. Monitor the task status
# 4. Guide you through approval when complete

# User says: "What tasks are pending?"
# This skill will:
# 1. Run ailang coordinator list --pending
# 2. Show interactive task explorer
# 3. Let you review diffs, logs, and approve/reject
```

## When to Use This Skill

Invoke this skill when:
- User asks to "delegate a task" or "send to coordinator"
- User wants to "check task status" or "see what's running"
- User asks to "review agent work" or "approve/reject tasks"
- User says "start the coordinator" or "stop the daemon"
- User wants to "clean up worktrees" or manage coordinator state

## Available Scripts

### `scripts/check_daemon.sh`
Check if the coordinator daemon is running and show status.

### `scripts/delegate_task.sh <type> <title> <description>`
Send a task to the coordinator for autonomous execution.

### `scripts/quick_status.sh`
Show a quick summary of pending, running, and completed tasks.

## Core Commands

### Starting/Stopping the Daemon

```bash
# Start coordinator + server (recommended)
make services-start

# Or just coordinator
ailang coordinator start

# Check status
ailang coordinator status

# Stop all
make services-stop
```

### Delegating Tasks

```bash
# Send a task
ailang messages send coordinator "Fix the null pointer bug in parser.go" \
  --title "Bug: Parser NPE" --from "claude-code" --type bug
```

### Monitoring & Approving

```bash
# Interactive task list
ailang coordinator list

# Filter by status
ailang coordinator list --pending
ailang coordinator list --running

# Approve from list: select task, press [a]
# Or directly: ailang coordinator approve <task-id>
```

## Task Lifecycle

```
pending → queued → running → pending_approval → completed
                          ↘ failed
                          ↘ rejected → [feedback] → pending (iteration 2) → running → ...
```

**Feedback Loop (v0.6.4+):** When rejecting, the task can be re-triggered with feedback up to 3 iterations. Claude uses `--resume` to continue with full conversation context.

## Unified Approvals (v0.6.5+)

When an agent has `trigger_on_complete` configured with `auto_approve_handoffs: false`, approvals are **combined**:

| Approval Type | Description | On Approve |
|--------------|-------------|------------|
| `merge` | Simple merge only | Merges code to dev branch |
| `merge_handoff` | Combined merge + handoff | Merges code AND triggers next agent |

**CLI display shows:**
```
⏳ [1] [merge+handoff] → sprint-planner  task-12345678
       Title: Agent completed work on: Fix parser bug
```

**What happens on approve:**
1. Code is merged to dev branch
2. Handoff message is sent to next agent's inbox with `session_id` for continuity
3. Worktree is cleaned up

**What happens on reject:**
1. Worktree is preserved
2. Feedback is sent to same agent's inbox
3. Agent resumes with `--resume <sessionId>` (same context, same worktree)
4. Iteration counter increments (max 3 attempts)

## GitHub-Driven Workflow (v0.6.2+)

For tasks linked to GitHub issues, the coordinator supports a fully GitHub-native approval workflow.

### How It Works

```
GitHub Issue
    ↓ (import)
DESIGN STAGE → posts design doc to GitHub → needs-design-approval label
    ↓ (human adds: design-approved)
SPRINT STAGE → posts sprint plan to GitHub → needs-sprint-approval label
    ↓ (human adds: sprint-approved)
IMPLEMENTATION → posts file changes → needs-merge-approval label
    ↓ (human adds: merge-approved)
Changes merged, issue auto-closed
```

### GitHub Labels Reference

| You Add This Label | What Happens |
|--------------------|--------------|
| `design-approved` | Advances to sprint planning |
| `sprint-approved` | Advances to implementation |
| `merge-approved` | Merges changes, closes issue |
| `needs-revision` | Pauses pipeline for changes |

### Quick Commands for GitHub Workflow

```bash
# Import GitHub issues as tasks
ailang messages import-github

# Check which issues are being watched
tail -100 ~/.ailang/logs/coordinator.log | grep -i "watching issue"

# Fallback: approve locally if labels aren't detected
ailang coordinator approve <task-id>

# Check pending approvals
ailang coordinator pending
```

### Why Use GitHub Workflow?

- **Review in GitHub UI** - See design docs and diffs alongside issue discussion
- **Mobile-friendly** - Approve from GitHub mobile app
- **Team collaboration** - Multiple reviewers can discuss in comments
- **Audit trail** - All approvals tracked in issue history

## Workflow

### 1. Delegate a Task

1. **Describe clearly** - Be specific about what needs to be done
2. **Choose type** - bug, feature, docs, research, refactor, test
3. **Send message** - `ailang messages send coordinator "..." --type bug`

### 2. Review Completed Work

1. **Open explorer** - `ailang coordinator list`
2. **Select task** - Enter task number
3. **Review**:
   - `[c]` View chat history (turn-by-turn conversation with tool calls)
   - `[d]` View diff
   - `[f]` Browse files
   - `[l]` View logs
4. **Decide**:
   - `[a]` Approve - merge changes to dev branch
   - `[r]` Reject - prompt for feedback, re-trigger task with context

### 3. Task Routing

| Type | Executor | Use Case |
|------|----------|----------|
| bug-fix | Claude Code | Code fixes |
| feature | Claude Code | New functionality |
| docs | Gemini | Documentation |
| research | Gemini | Investigation |
| script | Shell | Deterministic workflows (v0.6.4+) |

### 4. Script Agents (v0.6.4+)

For deterministic tasks that don't need AI inference:

```yaml
# In ~/.ailang/config.yaml
coordinator:
  agents:
    - id: echo-demo
      inbox: echo-demo
      invoke:
        type: script
        command: "./scripts/coordinator/echo_payload.sh"
        env_from_payload: true
        timeout: "1m"
      output_markers:
        - "ECHO_COMPLETE:"
```

**Test the demo:**
```bash
ailang messages send echo-demo '{"model": "gpt5", "benchmark": "fizzbuzz"}' \
  --title "Echo test" --from "user"
```

**What happens:**
- JSON `{"model": "gpt5"}` → env var `MODEL=gpt5`
- Nested JSON `{"db": {"host": "x"}}` → env var `DB_HOST=x`
- Auto-injected: `AILANG_TASK_ID`, `AILANG_MESSAGE_ID`, `AILANG_WORKSPACE`
- Cost: $0.00 (no AI inference)

## Auditing Agent Work

After a task completes, audit what the agent actually did before approving:

```bash
# View conversation per turn (shows agent reasoning + tool calls)
ailang coordinator logs <task-id> --limit 1000 --json | python3 -c "
import json, sys
data = json.load(sys.stdin)
events = data.get('events', [])
turns = {}; tools = {}
for evt in events:
    tn = evt.get('turn_num', 0); st = evt.get('stream_type', '')
    if st == 'text': turns.setdefault(tn, []).append(evt.get('text', ''))
    elif st == 'tool_use': tools.setdefault(tn, []).append(evt.get('tool_name', '?'))
for tn in sorted(turns.keys()):
    text = ''.join(turns[tn]).strip()
    if len(text) > 20:
        print(f'=== Turn {tn} (tools: {\", \".join(tools.get(tn, []))}) ===')
        print(text[:600]); print()
"

# View tool timeline with spans
ailang dashboard spans --task-id <task-id> --limit 200

# View git changes
ailang coordinator diff <task-id>
```

**Audit checklist:**
- [ ] Did the agent modify `internal/` code or just create examples/docs?
- [ ] What model was used? (Check `executor.model` in spans - Haiku may be too weak)
- [ ] Did it run `ailang run` (runtime test) or just `ailang check` (compile test)?
- [ ] Did it mark tasks as "already working" without verifying the specific bug scenario?

**Per-agent model config (v0.8.0+):**
Set `model: opus` in agent config for complex coding tasks:
```yaml
agents:
  - id: sprint-executor
    model: opus
```

## Troubleshooting

**Daemon won't start:** Check `ailang coordinator status`, then `make services-stop && make services-start`

**Task stuck:** View logs with `[l]` in task explorer

**Worktree limit:** `git worktree list` then `git worktree remove <path> --force`

**GitHub labels not detected:** The ApprovalWatcher may not be detecting labels. Use CLI fallback:
```bash
ailang coordinator pending    # List tasks waiting for approval
ailang coordinator approve <task-id>   # Approve locally (syncs label to GitHub)
```

**No logs from ApprovalWatcher:** Check coordinator logs for "GitHub approval watcher started". If missing, verify `~/.ailang/config.yaml` has `github_sync.enabled: true`.

## Resources

See [resources/reference.md](resources/reference.md) for complete CLI reference and advanced options.

## Notes

- Coordinator uses isolated git worktrees per task
- Worktrees auto-cleanup after approval
- Events stream to dashboard at http://localhost:1957
- State stored in `~/.ailang/state/coordinator.db`
