---
name: autonomous
description: Execute 1-2+ hour tasks autonomously with minimal supervision. Requires Task Contract (OUTCOME, EXCLUSIONS, DURATION, GUARDRAILS) upfront, then executes with clarification → plan → autonomous work → session report.
---

# Autonomous Mode

Execute extended tasks (1-2+ hours) without supervision after initial clarification.

## Prerequisites

User must provide a **Task Contract**:

```
OUTCOME: [What success looks like - measurable]
EXCLUSIONS: [What I will NOT do]
DURATION: [Time limit, e.g., "1 hour"]
GUARDRAILS: [Hard limits - code/logic to never touch]
```

## Execution Protocol

### Phase 1: Clarification (2-5 mins)

1. Read relevant files (issues-registry, SOURCE_OF_TRUTH, etc.)
2. Ask ONLY essential questions (1-3 max):
   - Prioritization questions
   - Ambiguity in scope
   - Items outside GUARDRAILS
3. User responds briefly

### Phase 2: Execution Plan

Show ordered task list:

```
Will execute in this order:
1. [Task 1] - [estimated time]
2. [Task 2] - [estimated time]
...

Estimated total: X mins
Strategy: [sequential/parallel/hybrid]

Ready to start.
```

Wait for user "go" or adjustments.

### Phase 3: Autonomous Execution

**Auto-behaviors:**

- Auto-invoke skills based on task type (no announcement)
- Auto-parallelize independent tasks
- Self-heal on errors (2-3 attempts before logging blocker)
- Update TodoWrite silently for progress tracking
- Batch accumulate learnings/issues in memory

**Skill auto-invocation map:**
| Task Type | Auto-Invoke |
|-----------|-------------|
| Bug fixing | `systematic-debugging` |
| Large feature (5+ files) | `brainstorming` → `writing-plans` |
| Multi-file changes | `writing-plans` → `executing-plans` |
| 3+ independent tasks | `dispatching-parallel-agents` |

**Error handling - Self-Heal First:**

```
Error encountered
    ↓
Attempt 1: Obvious fix
    ↓
Fail? → Attempt 2: Alternative approach
    ↓
Fail? → Attempt 3: Different angle
    ↓
Fail? → Log as BLOCKER, continue other tasks
```

**No interruptions except:**

- Genuine blocker (all approaches failed)
- GUARDRAILS violation detected
- DURATION limit reached

### Phase 4: Session End Report

```markdown
## AUTONOMOUS SESSION COMPLETE

**Duration:** X mins | **Progress:** Y% toward OUTCOME

### Completed

- ✅ [task 1]
- ✅ [task 2]

### Remaining

- ⏳ [task 3]

### Blockers (Need Your Input)

- 🚫 [blocker]: Tried [approach 1, 2, 3], all failed because [reason]

### Files Changed

- `path/file.ts` (lines X-Y): [what changed]

### Verification

- Type check: ✅ passed
- Build: ✅ passed
- Tests: [status]

### Knowledge Updates

- `learnings.md`: +N entries
- `issues-registry.md`: N bugs closed/updated
- `SOURCE_OF_TRUTH.md`: [section updated]

### Next Session Recommendation

[What to tackle next based on progress]
```

## Mid-Session Commands

User can send:

- `/status` - Brief progress update without stopping
- `/stop` - Halt immediately, give session report

Respond briefly to `/status` (2-3 lines), then continue working.

## Bypassed Requirements

In autonomous mode, the following normal requirements are BYPASSED:

| Bypassed                   | Why                            |
| -------------------------- | ------------------------------ |
| CLARITY GATE prompts       | Task Contract provides clarity |
| CHECKPOINT every 3 tasks   | No interruptions by design     |
| 5-section reports per task | Session-end report only        |
| "Quote the CLARITY GATE"   | Not needed                     |
| Ask before parallel agents | Auto-parallelized              |

| Still Enforced             | Why                 |
| -------------------------- | ------------------- |
| VERIFICATION before "done" | Quality control     |
| Type check after changes   | Catch errors early  |
| GUARDRAILS respect         | Safety boundary     |
| Knowledge file updates     | Done at session end |

## Guidelines

**DO:**

- Work silently and continuously
- Accumulate blockers, report at end
- Respect GUARDRAILS absolutely
- Self-heal errors before escalating
- Type check after every file change
- Update TodoWrite for progress
- Parallelize independent work

**DON'T:**

- Ask questions during execution phase
- Stop for checkpoints
- Touch code in GUARDRAILS
- Report 1-sentence updates
- Wait for approval between tasks
- Ignore errors (self-heal first)

## Trust Building Progression

| Phase    | Duration | Advance After         |
| -------- | -------- | --------------------- |
| Training | 30 mins  | 3 successful sessions |
| Short    | 1 hour   | 5 successful sessions |
| Medium   | 2 hours  | 3 successful sessions |
| Extended | 3+ hours | Earned trust          |

Start small, build confidence, expand scope.

## Example Session

```
USER:
AUTONOMOUS MODE

OUTCOME: All CRITICAL bugs in issues-registry.md fixed and verified
EXCLUSIONS: Not fixing MEDIUM/LOW, not adding features
DURATION: 1 hour
GUARDRAILS: Don't touch payment logic, don't change DB schema

CLAUDE:
I see 5 CRITICAL bugs. Questions:
1. BUG-003 requires a new API endpoint - is that within scope?
2. Should I prioritize revenue-impacting bugs first?

USER:
1. Yes, new endpoints are fine
2. Yes, revenue first

CLAUDE:
Execution plan:
1. BUG-001 (credit leak) - 15 mins
2. BUG-004 (payment race) - 20 mins
3. BUG-003 (API endpoint) - 15 mins
4. BUG-002, BUG-005 - 10 mins

Strategy: Sequential (bugs depend on each other)
Estimated: 50 mins

Ready to start.

USER:
go

[Claude works for 48 minutes]

CLAUDE:
## AUTONOMOUS SESSION COMPLETE
[Full session report as shown above]
```

## Success Criteria

Session is successful if:

- ✅ Made measurable progress toward OUTCOME
- ✅ Stayed within EXCLUSIONS
- ✅ Respected GUARDRAILS
- ✅ All code passes type check
- ✅ Blockers are clearly documented
- ✅ Knowledge files updated

## See Also

- `07-AUTONOMOUS_MODE.md` - Full documentation
- `02-ENFORCEMENT_CHECKLIST.md` - Bypass rules
- `01-USER_ENFORCEMENT_GUIDE.md` - User commands
