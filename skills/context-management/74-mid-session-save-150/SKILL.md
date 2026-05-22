---
name: 74-mid-session-save-150
description: "[74] CLOSE. Quick checkpoint during active work when context is running low. Use multiple times per development cycle to preserve progress and lessons. Lighter than close-session — no full handoff needed. Triggers on 'save progress', 'checkpoint', 'context low', or automatically when nearing token limits."
---

# Mid-Session Save 150 Protocol

**Core Principle:** Don't wait for session end to save. Checkpoint early, checkpoint often.

## What This Skill Does

This skill provides **quick checkpoints** during active work:
- Capture current progress without full handoff
- **Track what worked and what didn't** (raw material for lessons)
- Persist lessons learned so far
- Update session state for continuity
- Can be invoked **multiple times** per development cycle

### Key Insight: Progress Log as Lesson Source

The session progress log captures:
- ✅ What **worked** (successful approaches)
- ❌ What **didn't work** (failed attempts, dead ends)
- 🔄 What was **tried** (experiments, approaches tested)

This raw data becomes the source for extracting lessons later. Don't just save "what's done" — save the **journey** including failures.

## When to Use This Skill

**Triggers:**
- Context window running low (but not ending session)
- Significant progress made (feature partially done)
- Important lesson learned (don't risk losing it)
- Before complex/risky operation
- User says "save progress", "checkpoint", "зберегти"
- Every 30-45 min of active work (recommended cadence)

**NOT for:**
- Full session end → use `72-close-session-150`
- Just recording a single lesson → use `73-close-lessons-learn-150`

## The 150% Checkpoint Rule

- **100% Core:** What changed + current state
- **50% Enhancement:** Key learnings + immediate next step

## Quick Checkpoint Protocol

### Step 1: IDENTIFY CHANGES
What happened since last checkpoint:
- Files touched
- Decisions made
- Problems solved

### Step 2: LOG SESSION PROGRESS (Critical!)
Track the journey, not just the destination:
- ✅ **What worked** — successful approaches, solutions that fixed issues
- ❌ **What didn't work** — failed attempts, dead ends, wrong assumptions
- 🔄 **What was tried** — experiments, approaches tested, hypotheses
- 💡 **Why it worked/failed** — root cause understanding (if known)

**Write to:** `.session-context.md` in `## Progress Log` section
**Purpose:** Raw material for extracting lessons later

### Step 3: CAPTURE LESSONS (if ready)
If a clear lesson emerged:
- Add to MEMORY.md Lessons (Inbox)
- Don't skip this — context loss = lesson loss
- If lesson not yet clear, progress log will preserve the data

### Step 4: UPDATE SESSION STATE
Current state in MEMORY.md:
- Update `Session State` section
- Keep it brief and current

### Step 5: QUICK CONTEXT SAVE
Final state in `.session-context.md`:
- Current focus + next action
- Ready for immediate continuation

## Output Format: Mid-Session Checkpoint

```
⏱️ **MID-SESSION CHECKPOINT**

**Checkpoint:** #N | [HH:MM]
**Task:** [Current task name]

## Since Last Checkpoint
- [Change 1]
- [Change 2]

## Progress Log (What Worked / What Didn't)
✅ Worked:
- [Successful approach 1]
- [Solution that fixed issue]

❌ Didn't Work:
- [Failed attempt 1] — reason: [why it failed]
- [Dead end 2] — reason: [wrong assumption]

🔄 Tried:
- [Experiment/hypothesis tested]

## Current State
- Working on: [Current focus]
- Status: [Progress indicator]

## Lessons Captured
- [Lesson added to MEMORY.md, or "Pending — data in progress log"]

## Next Action
→ [Immediate next step]

---
✅ Checkpoint saved | Ready to continue
```

## Ultra-Quick Format

When time is very short (< 1 min):

```
⏱️ CHECKPOINT #N

Done: [What completed]
Worked: [What succeeded]
Failed: [What didn't work + why]
Now: [Current state]  
Next: [Immediate action]
```

## What Gets Updated

| Location | What | When |
|----------|------|------|
| `.session-context.md` | Quick state + **Progress Log** | Every checkpoint |
| `MEMORY.md` Session State | Current task | Every checkpoint |
| `MEMORY.md` Lessons (Inbox) | New learnings | Only if lessons are clear |

## Progress Log → Lessons Pipeline

```
Checkpoint #1: Log what worked/failed (raw data)
       ↓
Checkpoint #2: More data accumulated
       ↓
Checkpoint #3: Pattern emerges → Extract lesson → MEMORY.md Lessons (Inbox)
       ↓
Session End: Review all progress logs → Extract remaining lessons
```

**Key principle:** Not every checkpoint produces a lesson. The progress log is the **raw material** — lessons are **extracted** when patterns become clear.

## Checkpoint Cadence Recommendations

| Work Type | Recommended Interval |
|-----------|---------------------|
| Bug fixing | After each bug solved |
| Feature development | Every 30-45 min |
| Refactoring | After each file/component |
| Investigation | After major finding |
| Complex operation | Before and after |

## Comparison with Related Skills

| Skill | Purpose | When |
|-------|---------|------|
| `74-mid-session-save-150` | Quick checkpoint | During work, multiple times |
| `72-close-session-150` | Full handoff | End of session |
| `73-close-lessons-learn-150` | Record lesson | After success confirmation |

## Operational Rules

1. **CHECKPOINT OFTEN:** Better too many than too few
2. **LOG FAILURES TOO:** What didn't work is as valuable as what did
3. **LESSONS FIRST:** Don't lose learnings
4. **BE BRIEF:** Quick saves, not essays
5. **STAY CURRENT:** Update, don't accumulate
6. **IMMEDIATE NEXT:** Always know what's next
7. **PROGRESS = RAW DATA:** Not every checkpoint needs a lesson — collect data first

## Example: Development Cycle with Checkpoints

```
Start Session
    ↓
Load context (session-start-memory)
    ↓
Work on Feature Part 1
    ↓
⏱️ CHECKPOINT #1 (45 min in)
   └─ Progress: ✅ API route works | ❌ Hook failed (stale closure)
    ↓
Work on Feature Part 2
    ↓
⏱️ CHECKPOINT #2 (problem solved)
   └─ Progress: ✅ useCallback fixed closure | Pattern emerges → LESSON CAPTURED
    ↓
Work on Feature Part 3
    ↓
⏱️ CHECKPOINT #3 (context getting low)
   └─ Progress: 🔄 Trying SSR approach | ❌ hydration mismatch
    ↓
Continue or End Session
    ↓
Close session (close-session-150)
   └─ Review all progress logs → Extract lessons from ❌ patterns
```

### Example Progress Log Entry

```markdown
## Progress Log

### Checkpoint #1 — 14:30
✅ Worked:
- API route returns correct data
- Zod schema validates input

❌ Didn't Work:
- Direct state update in useEffect — caused infinite loop
- Reason: dependency array included computed object

🔄 Tried:
- useMemo for computed dependency — testing now

### Checkpoint #2 — 15:15
✅ Worked:
- useMemo solved the loop — stable reference now
- Component renders correctly

❌ Didn't Work:
- (none this round)

💡 Lesson extracted: "Never use computed objects in useEffect deps — use useMemo or extract IDs"
```

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **No checkpoints** | Lost context when resuming | Reconstruct from files, git, tests |
| **Stale checkpoint** | Info outdated | Update before continuing |
| **Lost lesson** | Repeated same mistake | Document with extra context |
| **Too verbose** | Checkpoint took too long | Use ultra-quick format |
| **Only logged success** | Repeated failed approach | Log ❌ failures with reasons |
| **No progress log** | Can't extract lessons at session end | Always log worked/didn't work |

---

**Remember:** Checkpoints are cheap. Lost context is expensive. When in doubt, checkpoint.
