---
name: reset
description: Reset after failures, blockers, or when stuck. Use when execution hits a wall, something breaks, or we need to step back and reassess. This is the fifth system in the 5-system framework.
---

# Reset System (Failure Recovery)

> **Purpose:** Gracefully recover from setbacks, learn, and continue.
> **When to trigger:** When stuck, something breaks, approach isn't working, or need to step back.

## Failure Response Protocol

### Step 1: STOP

**Immediately cease current approach.**

Do NOT:
- Try "one more thing"
- Keep pushing the same failing approach
- Make changes hoping they'll work
- Ignore the signals

Do:
- Acknowledge something isn't working
- Take a breath
- Prepare to capture state

### Step 2: CAPTURE STATE

Document what happened:

```markdown
## Failure Capture

**What we were trying to do:**
[Description of goal]

**What actually happened:**
[Description of failure/block]

**Error/symptom observed:**
[Specific error messages, unexpected behavior]

**What we tried:**
1. Attempt 1: [what] → [result]
2. Attempt 2: [what] → [result]
3. Attempt 3: [what] → [result]

**Current git state:**
[Branch, commit, uncommitted changes]
```

Log this to `.claude/failure-log.md`.

### Step 3: CHECKPOINT

Ensure state is preserved:

1. **Git status** - Are there uncommitted changes to save?
2. **Working state** - Note the last known working commit
3. **Context** - Save any important context that might be lost

```bash
git status
git stash  # if needed to preserve work-in-progress
```

### Step 4: DIAGNOSE

Determine the root cause category:

**Clarity Problem** (misunderstanding)
- Requirements were ambiguous
- Success criteria unclear
- Scope was wrong
→ Return to **Clarity System**

**Identity Problem** (hidden issue)
- Discovered unknown constraint
- Missed a dependency
- Technical limitation found
→ Run **Identity System**

**Priority Problem** (wrong focus)
- Solving the wrong problem
- This should have waited
- Dependencies not addressed
→ Return to **Priority System**

**Execution Problem** (bad approach)
- Approach was flawed
- Implementation strategy wrong
- Need different technique
→ Try different approach, same task

**External Block** (outside control)
- API down
- Missing credentials
- Need user input
→ Document and wait/ask

### Step 5: RESET TO APPROPRIATE SYSTEM

Based on diagnosis:

| Root Cause | Action |
|------------|--------|
| Clarity | Update active-context.md, restart with clarity |
| Identity | Run identification, log new issues |
| Priority | Re-evaluate, might deprioritize |
| Execution | New approach, same goal |
| External | Document, notify user, wait |

### Step 6: LEARN

Update `.claude/learnings.md` with:

```markdown
## Learning Entry - [Date]

**Failure:** [Brief description]

**Root Cause:** [What actually went wrong]

**Pattern:** [Is this a recurring issue?]

**Prevention:** [How to avoid this in future]

**New Rule/Check:** [Any process improvement to add]
```

## Failure Log Format

Maintain `.claude/failure-log.md`:

```markdown
# Failure Log

## Entry Template

| Date | Task | What Failed | Root Cause | Resolution | Learning |
|------|------|-------------|------------|------------|----------|
| 2026-01-01 | Add auth | Type errors cascaded | Didn't validate early | Reset, fix types first | Run tsc after every change |

## Detailed Entries

### [Date] - [Brief Title]

**Context:**
What we were doing

**Failure:**
What went wrong

**Attempts:**
What we tried

**Resolution:**
How it was fixed

**Takeaway:**
What we learned
```

## Recovery Strategies

### For Code Failures
1. `git stash` or commit current state
2. `git checkout .` to return to last working state
3. Re-approach with new strategy

### For Conceptual Failures
1. Step back to clarity
2. Re-read requirements
3. Ask user for clarification

### For Integration Failures
1. Isolate the failing component
2. Test in isolation
3. Gradually reintegrate

### For Persistent Failures
1. Document thoroughly
2. Ask user for help
3. Consider if this is the right approach at all

## Rules

1. **No shame in reset** - It's better to restart cleanly than compound mistakes
2. **Document first** - Don't reset without capturing what happened
3. **Learn always** - Every failure is information
4. **Stay calm** - Frustration compounds errors
5. **Ask for help** - The user is a partner, not a judge

## Transition

After reset:
- Clarity problem → **Clarity System**
- Hidden issue found → **Identity System**
- Wrong priority → **Priority System**
- Bad approach → **Execution System** with new approach
- Resolved → Continue with task

---

*This is System 5 of 5: Clarity → Identity → Priority → Execution → Reset*

## The Complete Cycle

```
          ┌─────────────────────────────────────────────┐
          │                                             │
          ▼                                             │
    ┌─────────┐     ┌──────────┐     ┌──────────┐      │
    │ CLARITY │ ──▶ │ IDENTITY │ ──▶ │ PRIORITY │      │
    └─────────┘     └──────────┘     └──────────┘      │
                                           │            │
                                           ▼            │
                                    ┌───────────┐       │
                                    │ EXECUTION │       │
                                    └───────────┘       │
                                           │            │
                              ┌────────────┴────────┐   │
                              ▼                     ▼   │
                        ┌─────────┐           ┌───────┐ │
                        │ FAILURE │           │SUCCESS│ │
                        │ (Reset) │           └───────┘ │
                        └─────────┘                     │
                              │                         │
                              └─────────────────────────┘
```
