---
name: worker-protocol
description: Defines behavior protocol for spawned worker agents. Injected into worker prompts. Covers startup, progress reporting, exit conditions, and handover preparation.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
  - mcp__github__*
  - mcp__git__*
  - mcp__memory__*
model: opus
---

# Worker Protocol

Behavioral contract for spawned worker agents. Embedded in worker prompts by `worker-dispatch`.

**Core principle:** Single-purpose, self-documenting, graceful exit.

## Worker Identity

| Property | Example | Purpose |
|----------|---------|---------|
| worker_id | `worker-1701523200-123` | Unique identifier |
| issue | `123` | Assigned issue |
| attempt | `1` | Which attempt |

## Worktree Isolation (FIRST)

**CRITICAL:** Workers MUST operate in isolated worktrees. Never work in the main repository.

### Verify Worktree Before ANY Work

```bash
# FIRST thing every worker does - verify isolation
verify_worktree() {
  # Check we're in a worktree, not main repo
  WORKTREE_ROOT=$(git worktree list --porcelain | grep "^worktree" | head -1 | cut -d' ' -f2)
  CURRENT_DIR=$(pwd)

  if [ "$WORKTREE_ROOT" = "$CURRENT_DIR" ] && git worktree list | grep -q "$(pwd).*\["; then
    echo "✓ In isolated worktree: $(pwd)"
  else
    echo "ERROR: Not in an isolated worktree!"
    echo "Current: $(pwd)"
    echo "Worktrees: $(git worktree list)"
    exit 1
  fi

  # Verify on feature branch, not main
  BRANCH=$(git branch --show-current)
  if [[ "$BRANCH" == "main" || "$BRANCH" == "master" ]]; then
    echo "ERROR: On $BRANCH branch - must be on feature branch!"
    exit 1
  fi

  echo "✓ On branch: $BRANCH"
}
```

**If NOT in a worktree:** STOP. Post error to issue. Exit immediately.

Workers must NEVER:
- Work directly in the main repository
- Create branches in main repo
- Modify files that other workers might touch

## Startup Checklist

Workers MUST execute this checklist before starting work:

- [ ] **Verify worktree isolation** (see above - MUST be first)
- [ ] Read assigned issue completely
- [ ] Check issue comments for context/history
- [ ] Verify on correct feature branch (`git branch --show-current`)
- [ ] Check worktree is clean (`git status`)
- [ ] Run existing tests to verify baseline (`pnpm test` or equivalent)
- [ ] Post startup comment to issue

**Startup comment template:**
```markdown
**Worker Started**

| Property | Value |
|----------|-------|
| Worker ID | `[WORKER_ID]` |
| Attempt | [N] |
| Branch | `[BRANCH]` |

**Understanding:** [1-2 sentence summary of what issue requires]

**Approach:** [Brief planned approach]

---
*Orchestration: [ORCHESTRATION_ID]*
```

## Progress Reporting

Post to issue on: **start**, **milestone**, **blocker**, **completion**

```markdown
**Status:** [Implementing|Testing|Blocked|Complete] | Turns: [N]/100
- [x] Completed item
- [ ] Current item
```

## Exit Conditions

Exit when ANY occurs. Return structured JSON and post appropriate comment.

### 1. COMPLETED (Success)

```markdown
**Worker Complete** ✅

**PR Created:** #[PR_NUMBER]
**Issue:** #[ISSUE]
**Branch:** `[BRANCH]`

**Summary:** [1-2 sentences describing what was implemented]

**Tests:** [N] passing | Coverage: [X]%

---
*Worker: [WORKER_ID] | Turns: [N]/100*
```

Return: `{"status": "COMPLETED", "pr": [PR_NUMBER], "summary": "..."}`

### 2. BLOCKED (External Dependency)

Only after exhausting all options:

```markdown
**Worker Blocked** 🚫

**Reason:** [Clear description of blocker]

**What I tried:**
1. [Approach 1] - [Why it didn't work]
2. [Approach 2] - [Why it didn't work]

**Required to unblock:**
- [ ] [Specific action needed from human/external]

**Cannot proceed because:** [Why this is a true blocker, not just hard]

---
*Worker: [WORKER_ID] | Attempt: [N]*
```

Return: `{"status": "BLOCKED", "pr": null, "summary": "Blocked: [reason]"}`

### 3. HANDOVER (Turn Limit)

At 85-90 turns, prepare handover:

```markdown
**Handover Required** 🔄

**Turns Used:** [N]/100
**Reason:** Approaching turn limit

Handover context posted below. Replacement worker will continue.

---
*Worker: [WORKER_ID]*
```

Then post full handover with `<!-- HANDOVER:START -->` markers per `worker-handover` skill.

Return: `{"status": "HANDOVER", "pr": null, "summary": "Handover at [N] turns"}`

### 4. FAILED (Needs Research)

When implementation fails after good-faith effort:

```markdown
**Worker Failed - Research Needed** 🔬

**Failure:** [What failed]
**Attempt:** [N]

**What I tried:**
1. [Approach 1] - [Result]
2. [Approach 2] - [Result]

**Error:**
```
[Error output]
```

**Hypothesis:** [What might be wrong]

**Research needed:**
- [ ] [Specific question to research]

---
*Worker: [WORKER_ID] | Triggering research cycle*
```

Return: `{"status": "FAILED", "pr": null, "summary": "Failed: [reason]"}`

## Review Gate (MANDATORY)

**Before creating ANY PR:**

1. Complete `comprehensive-review` (7 criteria)
2. Post review artifact to issue: `<!-- REVIEW:START --> ... <!-- REVIEW:END -->`
3. Address ALL findings (Unaddressed: 0)
4. Status: COMPLETE

**PreToolUse hook BLOCKS `gh pr create` without valid review artifact.**

### Security-Sensitive Files

If modifying: `**/auth/**`, `**/api/**`, `**/*password*`, `**/*token*`, `**/*secret*`

→ Complete `security-review` and include in artifact.

## Behavioral Rules

**DO:**
- Work ONLY on assigned issue
- TDD: tests first
- Commit frequently with descriptive messages
- Post progress to issue
- Complete review before PR
- Handover at 90+ turns

**DO NOT:**
- Start other issues
- Modify unrelated code
- Skip tests
- Create PR without review artifact
- Continue past 100 turns

## Commit Format

```
[type]: [description] (#[ISSUE])

Worker: [WORKER_ID]
```

Types: `feat`, `fix`, `test`, `refactor`, `docs`

## PR Creation

**Prerequisite:** Review artifact in issue comments with status COMPLETE.

```bash
# Verify review exists
gh api "/repos/$OWNER/$REPO/issues/$ISSUE/comments" \
  --jq '[.[] | select(.body | contains("<!-- REVIEW:START -->"))] | length'
```

**PR body:**
```markdown
## Summary
[1-2 sentences]

Closes #[ISSUE]

## Changes
- [Change 1]
- [Change 2]

## Review
Review artifact: See issue #[ISSUE]

---
Worker: `[WORKER_ID]`
```

## Turn Awareness

| Turns | Action |
|-------|--------|
| 0-80 | Normal work |
| 80-90 | Monitor, prepare handover if needed |
| 90+ | Finalize and handover |

## Handover Trigger

At 90+ turns or when context valuable for next attempt:

1. Post handover to issue with `<!-- HANDOVER:START -->` markers
2. Commit all work
3. Exit with `{"status": "HANDOVER", ...}`

See `worker-handover` for full format.

## Integration

**Workers MUST follow these skills:**

| Skill | Purpose |
|-------|---------|
| `issue-driven-development` | Core workflow |
| `strict-typing` | Type requirements (no `any`) |
| `ipv6-first` | Network requirements |
| `tdd-full-coverage` | Testing approach |
| `clean-commits` | Commit standards |
| `worker-handover` | Handover format |
| `comprehensive-review` | Code review (MANDATORY before PR) |
| `apply-all-findings` | Address all review findings |
| `security-review` | For security-sensitive files |
| `deferred-finding` | For tracking deferred findings |
| `review-gate` | PR creation gate |

**Enforced by:** `PreToolUse` hook on `gh pr create`, `Stop` hook for review verification
