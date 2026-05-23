---
name: shared-context-management
description: Context window auto-reset procedures for Ralph agents. Use when context approaches 70% capacity during long tasks. Use proactively to monitor token usage and create checkpoints.
category: infrastructure
tags: [context, reset, checkpoint, memory]
dependencies: [shared-ralph-core, shared-atomic-updates]
---

# Context Window Management

> "Your context will fill up after many iterations – monitor, checkpoint, reset, continue."

## When to Use This Skill

Use **when**:
- Context approaches 70% capacity
- Starting a big task (5+ acceptance criteria, 3+ files, architectural)
- After completing many file operations

Use **proactively**:
- Check context with `/context` command periodically
- Create checkpoints before context reset
- Verify resumption after reset

---

## Quick Start

<examples>
Example 1: Check context during big task
```
/context
# Shows: Total: 140,000 / 200,000 = 70% → Time to checkpoint!
```

Example 2: Create checkpoint before reset
```powershell
Send-Message -To "watchdog" -Type "System" -Payload @{
    systemEvent = "context_checkpoint"
    contextPercent = 72
    taskId = "feat-001"
    completedSteps = @("research", "implement")
    remainingSteps = @("test", "commit")
}
# Also write: .claude/session/context-checkpoint-developer-feat-001.json
```

Example 3: Resume after context reset
```bash
# Read checkpoint file
cat .claude/session/context-checkpoint-developer-feat-001.json
# Skip completed steps, continue from nextAction
```
</examples>

---

## The Problem

Context overflow causes:
- Slower responses
- Forgetting earlier instructions
- Inconsistent behavior

---

## Task Complexity Detection

| Indicators | Action |
|------------|--------|
| **Big task** (5+ acceptance criteria, 3+ files, architectural) | Monitor context, checkpoint at 70% |
| **Small task** (single file, bug fix, simple refactor) | Skip monitoring |

---

## Context Threshold

**70% capacity = 140,000 tokens**

```
total_input_tokens + total_output_tokens = total usage
total usage / 200,000 = percentage
```

If >= 70%: Create checkpoint and prepare for reset.

---

## Checkpoint Format

```powershell
# Via named pipe (agent-runtime.ps1)
Send-Message -To "watchdog" -Type "System" -Payload @{
    systemEvent = "context_checkpoint"
    reason = "context_limit_approached"
    contextPercent = 72
    taskId = $taskId
    step = "current_step_name"
    completedSteps = @("step1", "step2")
    remainingSteps = @("step3", "step4")
    filesModified = @("src/file1.ts", "src/file2.ts")
    nextAction = "what to do next"
    prerequisiteState = @{
        branch = "git_branch"
        filesCreated = @()
        commitsMade = 1
    }
}
```

**Also write**: `.claude/session/context-checkpoint-{agent}-{taskId}.json`

---

## Worker Resumption

When restarting after context reset:

1. **Check for checkpoint**: `.claude/session/context-checkpoint-{agent}-{taskId}.json`
2. **Read checkpoint state**:
   - `completedSteps` - Already done
   - `remainingSteps` - What's left
   - `filesModified` - Files touched
   - `nextAction` - Immediate action
3. **Resume work**: Skip completed, continue from `nextAction`
4. **Clean up checkpoint** after task completes

---

## Check Schedule

For big tasks, check context every N operations:

| Operation Type | Check Frequency |
|----------------|-----------------|
| File reads | Every 10 reads |
| File writes | Every 3 writes |
| Code generation | Every 2 edits |
| Tool calls | Every 5 calls |
| After sub-agent | Always check |

---

## Before Restarting

| Agent | Ensure Saved |
|-------|--------------|
| **PM** | All task statuses updated, session current |
| **Developer** | Changes committed, task status updated |
| **QA** | Validation committed, bugs logged |

---

## State File Persistence

Files that survive context resets:

| File | Purpose | Survives |
|------|---------|----------|
| `prd.json` | Tasks, session, agent status | ✅ |
| `context-checkpoint-*.json` | Mid-task checkpoint | ✅ |
| `retrospective.txt` | Active retrospective | ✅ |

---

## What You Can Forget

After restart, safely forget:
- Past task implementation details
- Past retrospective discussions
- Old file contents
- Completed task specs
- Historical transcripts

---

## Verification

```bash
/context                                  # Check current usage
cat .claude/session/context-reset-count.txt  # Should increment
```

Verify `iteration` counter in `prd.json.session` continues across resets.

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-core` | Session structure, status values |
| `shared-atomic-updates` | Safe file updates |
| `shared-worker-protocol` | Worker exit patterns |
