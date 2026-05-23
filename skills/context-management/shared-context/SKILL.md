---
name: context-management
description: Context window auto-reset procedures for Ralph agents. Use when context fills up during long tasks.
user-invocable: true
---

# Context Window Management

> "Your context will fill up after many iterations. Use `/context` to monitor and checkpoints to continue."

**IMPORTANT FOR EVENT-DRIVEN MODE:**
Use native Read/Write tools for all message operations. Messages are stored as JSON files in `.claude/session/messages/`.

## The Problem

After implementing many features or running many iterations, your context window will fill up. This causes:

- Slower responses
- Forgetting earlier instructions
- Inconsistent behavior

## Context Checking Procedure

### Built-in Context Check

Use the `/context` command to check your current token usage:

```
/context
```

**Output interpretation:**

- `total_input_tokens` + `total_output_tokens` = your total usage
- Divide by 200,000 for percentage
- If >= 70% (140,000 tokens): Create checkpoint and exit

**Example:**

```
Input:  95,432 tokens
Output: 44,567 tokens
Total:  140,000 / 200,000 = 70% → Time to checkpoint!
```

## Task Complexity Detection

**Big task indicators (ENABLE context monitoring):**

- Task has 5+ acceptance criteria
- Task requires 3+ files to be created/modified
- Task category is `architectural` or `integration`
- Estimated to take > 10 operations

**Small task indicators (SKIP context monitoring):**

- Single file change
- Bug fix with clear scope
- Simple refactor
- Estimated to take < 5 operations

## Context Checkpoint Format

When context >= 70%, send this message to supervisor:

```json
// Write to: .claude/session/messages/supervisor/cmd/{timestamp}.json
{
  "id": "msg-context-checkpoint-{timestamp}",
  "from": "{your-agent}",
  "to": "supervisor",
  "type": "context_checkpoint",
  "payload": {
    "reason": "context_limit_approached",
    "contextPercent": 72,
    "taskId": "{taskId}",
    "step": "{current_step_name}",
    "completedSteps": ["step1", "step2"],
    "remainingSteps": ["step3", "step4"],
    "filesModified": ["src/file1.ts", "src/file2.ts"],
    "nextAction": "{what to do next}",
    "prerequisiteState": {
      "branch": "{git_branch}",
      "filesCreated": [],
      "commitsMade": 1
    }
  },
  "timestamp": "{ISO-8601-UTC}"
}
```

**Also write checkpoint file:** `.claude/session/context-checkpoint-{agent}-{taskId}.json`

This allows the restarted agent to know exactly where to continue.

## Worker Resumption After Context Reset

When restarting after context reset:

1. **Check for checkpoint file:**

   ```bash
   # Look for: .claude/session/context-checkpoint-{agent}-{taskId}.json
   # Use Glob tool to find the file
   ```

2. **Read checkpoint state:**
   - `completedSteps` - What's already done
   - `remainingSteps` - What still needs to be done
   - `filesModified` - Files already touched
   - `nextAction` - What to do immediately

3. **Resume work:**
   - Skip completed steps
   - Continue from `nextAction`
   - No need to re-read files already processed (state in PRD)

4. **Clean up checkpoint** after task completes

## Periodic Context Check Schedule

**For big tasks, check context every N operations:**

| Operation Type  | Check Frequency |
| --------------- | --------------- |
| File reads      | Every 10 reads  |
| File writes     | Every 3 writes  |
| Code generation | Every 2 edits   |
| Tool calls      | Every 5 calls   |
| After sub-agent | Always check    |

**Simplified rule:** After every significant action (file write, edit, commit), ask yourself:
"Is this a big task? If so, check context."

## Before Restarting

Ensure your work is saved:

### PM Coordinator

- All tasks have updated status in `prd.json`
- `prd.json.session` is current
- No task is mid-assignment (complete or defer)

### Developer

- All changes committed to git
- Task status updated in `prd.json.agents.developer`
- No implementation mid-progress

### QA

- Validation results committed to PRD (`passes` field updated)
- Task status updated in `prd.json.agents.qa`
- All bugs logged in `prd.json.items[{taskId}]` if any

## After Restart

The new session will automatically reload essential state:

```
READ prd.json
```

Continue from where you left off. All session state (iteration, stats) and task details are now stored in `prd.json`.

## What You Need to Resume

You only need these files to resume:

- `prd.json` - Task list, session state, and agent status (all in one file)
- `context-checkpoint-{agent}-{taskId}.json` - If mid-task checkpoint was created

## What You Can Forget

After restart, you can safely forget:

- Past task implementation details
- Past retrospective discussions
- Old file contents you've read
- Completed task specifications
- Historical discussion transcripts

## Minimal Context Footprint

**Keep:**

- Current task specifications
- Currently edited files
- Quality mindset and coding standards
- Feedback loop commands
- Session state (iteration, stats)

**Don't keep:**

- Completed task file contents
- Past task specifications
- Historical discussion transcripts
- Past retrospective details (logged in files)

## State File Persistence

These files survive across context resets:

| File                                       | Purpose                                | Survives Reset |
| ------------------------------------------ | -------------------------------------- | -------------- |
| `prd.json`                                 | Task list, session state, agent status | ✅ Yes         |
| `context-checkpoint-{agent}-{taskId}.json` | Mid-task checkpoint (if created)       | ✅ Yes         |
| `retrospective.txt`                        | Active retrospective                   | ✅ Yes         |
| `persistent-state/consolidation-mode.json` | Consolidation mode state               | ✅ Yes         |

### Consolidation Mode State Preservation

**Consolidation mode state is automatically preserved across context resets.**

When PM agent context is reset:

1. Consolidation mode state is saved to `persistent-state/consolidation-mode.json`
2. After reset, PM automatically restores consolidation mode
3. This prevents workers from being blocked after context resets

**Manual Recovery (if needed):**

In EVENT-DRIVEN mode, consolidation state is automatically saved to `persistent-state/consolidation-mode.json` before context resets and restored after.

**To manually save/restore consolidation state:**

Use the bash-safe helper:

```bash
# Save state
source ./.claude/scripts/pwsh-helper.sh
# (Consolidation state is auto-saved in mq-ops.ps1)

# Or directly check the state file
cat persistent-state/consolidation-mode.json
```

## Verification

To verify context reset is working:

1. Run `/context` to see current token usage
2. Check `.claude/session/context-reset-count.txt` - should increment on each reset
3. Check that `iteration` counter in `prd.json.session` continues across resets
4. Verify agent continues working from where it left off

## Reference

- [shared-core.md](shared-core.md) — Session structure
- [shared-messaging.md](shared-messaging.md) — Event-driven messaging protocol
