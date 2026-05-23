---
name: finish-work
description: Mandatory gate for ending work sessions. Checks if minimum work duration has elapsed before allowing completion. ALWAYS use this skill before claiming work is complete.
---

# Finish-Work Gate

**MANDATORY:** Use this skill BEFORE claiming work is complete, before creating final commits, or before ending any work session.

## Purpose

Prevents early work termination by enforcing minimum work durations. The agent does not have permission to declare work complete without passing through this gate.

## Relationship to Other "Finish" Tools

**Different scopes - use in sequence:**

| Tool | Scope | When to Use |
|------|-------|-------------|
| `finish-work` skill | **Session-level** | Check time gate BEFORE any completion |
| `/finish` command | **Documentation** | Create handoff docs AFTER time gate passed |
| `finishing-a-development-branch` | **Branch-level** | Git workflow (merge/PR/discard) AFTER work complete |
| `verification-before-completion` | **Quality** | Verify tests/evidence BEFORE declaring done |

**Correct sequence:**
```
Work Session
  → finish-work skill (time gate check - must pass first)
    → verification-before-completion (quality check)
      → /finish command (handoff documentation)
        → finishing-a-development-branch (git workflow - if applicable)
```

**Important:** 
- `/finish` assumes work is complete - it doesn't check time gate. Run `finish-work` FIRST.
- `finishing-a-development-branch` is for branch management after work is truly done.

## The Iron Rule

```
NO WORK COMPLETION WITHOUT PASSING THE FINISH-WORK GATE
```

## How to Use

### Checkpoint Mode (During Long Sessions)

Every ~30 minutes of work, run a quick checkpoint:

```powershell
$manifest = Get-Content .session_manifest.json | ConvertFrom-Json
$start = [DateTime]$manifest.started
$now = Get-Date
$elapsed = $now - $start
$remaining = $manifest.minimum_minutes - $elapsed.TotalMinutes
Write-Host "⏰ Checkpoint: $([int]$remaining) minutes remaining until $($manifest.target_end)"
```

**Purpose:** Keeps the time commitment fresh in your mind. Cheap insurance against forgetting.

### When You Think You're Done

#### Step 1: Check for Bypass Attempts

**STOP if you find yourself thinking or typing:**
- "Work is complete"
- "I'm done"  
- "Finished"
- "Wrapping up"
- "Session complete"

**If you haven't run finish-work skill yet, you're trying to bypass the gate.**

#### Step 2: Read Session Manifest
```bash
Get-Content .session_manifest.json | ConvertFrom-Json
```

#### Step 3: Calculate Elapsed Time
```powershell
$manifest = Get-Content .session_manifest.json | ConvertFrom-Json
$start = [DateTime]$manifest.started
$now = Get-Date
$elapsed = $now - $start
$remaining_minutes = $manifest.minimum_minutes - $elapsed.TotalMinutes
```

#### Step 4: Gate Decision

**IF remaining_minutes > 0:**
```
⏰ SESSION INCOMPLETE - CONTINUE WORKING

Started: {start_time}
Target:  {target_end}
Elapsed: {elapsed_minutes} minutes
Minimum: {minimum_minutes} minutes
Remaining: {remaining_minutes} minutes

YOU MAY NOT FINISH YET.

Find more work to do:
- Review the codebase for issues
- Add documentation
- Run additional tests
- Refactor for clarity
- Add error handling
- Improve comments
- Check for edge cases
- Optimize performance
- Add logging
- Review similar implementations for patterns

DO NOT stop working. Continue until time elapsed.
```

**IF remaining_minutes <= 0 OR manifest is missing:**
```
✅ SESSION COMPLETE

Minimum duration met. Proceed with:
1. Final verification (run tests)
2. Clean commits
3. Push to origin
4. Session summary
```

## Session Manifest Format

File: `.session_manifest.json` (in project root)

```json
{
  "session_id": "unique-name",
  "started": "2026-01-27T23:00:00",
  "target_end": "2026-01-28T01:00:00",
  "minimum_minutes": 120,
  "reason": "Why this work block exists",
  "hard_stop": true,
  "created_by": "user"
}
```

### Fields
- `session_id`: Unique identifier for this work block
- `started`: ISO timestamp when work began
- `target_end`: ISO timestamp when work should end
- `minimum_minutes`: Minimum work duration (enforced)
- `reason`: Purpose of this work block
- `hard_stop`: If true, cannot finish before minimum_minutes
- `created_by`: Who created the session (user or agent)

## Context Recovery (REQUIRED)

### When to Recover

**RE-READ the manifest when:**
1. You see "Continuing from previous..." (context was compacted)
2. System restarted or new process started
3. You don't remember the target end time
4. You feel "done" but aren't sure if enough time passed
5. Any interruption occurred

### Recovery Procedure

```powershell
# ALWAYS re-read after context loss
$manifest = Get-Content .session_manifest.json | ConvertFrom-Json
$start = [DateTime]$manifest.started
$now = Get-Date
$elapsed = $now - $start
$remaining = $manifest.minimum_minutes - $elapsed.TotalMinutes

Write-Host "✓ RECOVERY: Session manifest re-read"
Write-Host "  Working until: $($manifest.target_end)"
Write-Host "  Elapsed: $([int]$elapsed.TotalMinutes) minutes"
Write-Host "  Remaining: $([int]$remaining) minutes"
```

**Cost:** ~30 tokens to re-read
**Benefit:** Prevents hours of lost work from stopping early

### Why This Matters

Context compaction destroys the "I checked at start" memory. Without recovery:
- Agent forgets time commitment
- Agent stops early thinking work is done
- Violates user trust

**Rule:** When in doubt, re-read the manifest.

## If Manifest Is Missing

**Create one immediately:**
```powershell
@{
  session_id = "recovery-$(Get-Random)"
  started = (Get-Date).ToString("o")
  target_end = (Get-Date).AddHours(2).ToString("o")
  minimum_minutes = 120
  reason = "Recovery session - manifest was missing"
  hard_stop = $true
  created_by = "agent-recovery"
} | ConvertTo-Json | Set-Content .session_manifest.json
```

Then continue working.

## Why This Matters

Early stopping wastes:
- **Context** built up during work
- **Human time** spent reviewing incomplete work
- **Opportunity** to catch issues with fresh eyes
- **Trust** when claims of completion are false

The finish-work gate ensures:
- Work blocks are honored
- Sufficient time for quality
- No premature "completion" claims
- Respect for time commitments

## Common Rationalizations (REJECT THESE)

| Excuse | Reality |
|--------|---------|
| "I'm done with the task" | There's always more to do (docs, tests, polish) |
| "No more work to do" | Look harder - edge cases, cleanup, validation |
| "I've been working hard" | Elapsed time ≠ Worked time, keep going |
| "The tests pass" | Great, now add more tests, review, document |
| "I need a break" | Not an option until time elapsed |
| "I'll finish tomorrow" | Violates the commitment made |

## The Bottom Line

**Work the full duration. No exceptions. This skill enforces that.**

If the gate says continue: YOU CONTINUE.

---

*This skill is non-negotiable. Use it every time.*
