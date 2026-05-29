---
name: phase-protocol
description: |
  Phase execution protocol to prevent context drift during long development sessions.
  MUST be read at the start of each phase and referenced in the last TODO of each phase.
  This ensures AI maintains context across phases.
---

# Phase Protocol

## Purpose

This protocol prevents context drift during long development sessions by:
1. **Entry Gate** - Forcing context refresh at phase start
2. **TODO anchoring** - Creating TODO immediately to survive context compression
3. **Exit Gate** - Forcing re-read of this protocol before next phase

**Key insight:** Once TODO is created, it survives context compression. By creating TODO early with Exit Gate that re-reads this protocol, we ensure the loop continues.

---

## Phase Entry Protocol

**Execute these steps IN ORDER at the start of each phase:**

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE N ENTRY PROTOCOL                                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Step 1: READ THIS SKILL (current step - context refresh)         │
│         → You are doing this now                                 │
│                                                                   │
│ Step 2: READ tasks.md                                            │
│         → Get task list for current phase                        │
│         → Identify which phase you are entering                  │
│                                                                   │
│ Step 3: CREATE TODO IMMEDIATELY ← 🔴 CRITICAL!                   │
│         → Use TodoWrite tool NOW                                 │
│         → Include: Entry Gate + Tasks + Exit Gate                │
│         → This MUST happen BEFORE reading other docs!            │
│         → Reason: TODO survives context compression              │
│                                                                   │
│ Step 4: GATE - Verify TODO completeness                          │
│         → Count items: Entry (8) + Tasks (N) + Exit (3)          │
│         → If incomplete → add missing items NOW                  │
│                                                                   │
│ Step 5: READ plan.md                                             │
│         → Understand implementation approach                     │
│                                                                   │
│ Step 6: READ design.md                                           │
│         → Understand technical decisions                         │
│                                                                   │
│ Step 7: READ specs/*.md                                          │
│         → Understand requirements and scenarios                  │
│                                                                   │
│ Step 8: GATE - Output key understanding                          │
│         → Must output before proceeding                          │
│         → Format provided below                                  │
│                                                                   │
│ Step 9: BEGIN IMPLEMENTATION                                     │
│         → Now you can start actual development                   │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## TODO Structure Template

**When creating TODO in Step 3, use this structure:**

```markdown
=== Phase N: [Phase Name] ===

--- ENTRY GATE (complete first) ---
- [ ] PN-Gate-1: Read phase-protocol skill (current)
- [ ] PN-Gate-2: Read tasks.md
- [ ] PN-Gate-3: Create Phase N TODO (current)
- [ ] PN-Gate-4: [GATE] Verify TODO completeness
- [ ] PN-Gate-5: Read plan.md
- [ ] PN-Gate-6: Read design.md
- [ ] PN-Gate-7: Read specs/*.md
- [ ] PN-Gate-8: [GATE] Output key understanding

--- IMPLEMENTATION TASKS ---
- [ ] PN-1: [Task from tasks.md]
- [ ] PN-2: [Task from tasks.md]
- [ ] PN-3: [Task from tasks.md]
...

--- EXIT GATE (complete after all tasks) ---
- [ ] PN-Exit-1: Update tasks.md (mark completed)
- [ ] PN-Exit-2: Git commit
- [ ] PN-Exit-3: Re-read phase-protocol + Create Phase N+1 TODO ← 🔄
```

**Replace:**
- `N` with phase number (1, 2, 3...)
- `[Phase Name]` with actual phase name
- `[Task from tasks.md]` with actual tasks

---

## Gate Verification Templates

### Gate-4: TODO Completeness Verification

**Output this checklist BEFORE proceeding:**

```markdown
🚧 PHASE N TODO COMPLETENESS CHECK 🚧

Entry Gate items: [count] (expected: 8)
□ PN-Gate-1: Read phase-protocol skill
□ PN-Gate-2: Read tasks.md
□ PN-Gate-3: Create TODO
□ PN-Gate-4: Verify TODO completeness
□ PN-Gate-5: Read plan.md
□ PN-Gate-6: Read design.md
□ PN-Gate-7: Read specs/*.md
□ PN-Gate-8: Output key understanding

Implementation items: [count]
□ [List all task items]

Exit Gate items: [count] (expected: 3)
□ PN-Exit-1: Update tasks.md
□ PN-Exit-2: Git commit
□ PN-Exit-3: Re-read protocol + Create next TODO

TOTAL: [8 + N + 3] items

✅ Complete - proceeding to Step 5
🚫 Incomplete - adding missing items NOW
```

### Gate-8: Key Understanding Confirmation

**Output this summary BEFORE starting implementation:**

```markdown
🚧 PHASE N KEY UNDERSTANDING 🚧

## Phase Goal
[1-2 sentences describing what this phase accomplishes]

## Tasks to Complete
1. [Task 1 brief description]
2. [Task 2 brief description]
3. [Task 3 brief description]

## Spec References
- Requirement: [Name] → Scenario: [Name]
- Requirement: [Name] → Scenario: [Name]

## Technical Approach (from design.md)
- [Key decision 1]
- [Key decision 2]

## Files to Create/Modify
- Create: [file paths]
- Modify: [file paths]

✅ Understanding confirmed - beginning implementation
🚫 Unclear - re-reading documents
```

---

## Phase Exit Protocol

**Execute these steps IN ORDER after completing all phase tasks:**

```
┌─────────────────────────────────────────────────────────────────┐
│ PHASE N EXIT PROTOCOL                                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ Step 1: UPDATE tasks.md                                          │
│         → Mark all completed tasks [x]                           │
│         → Update Status counts                                   │
│         → Update Completion Tracking table                       │
│                                                                   │
│ Step 2: GIT COMMIT                                               │
│         → Stage all changes                                      │
│         → Commit with descriptive message                        │
│         → Include Spec references                                │
│                                                                   │
│ Step 3: CHECK - More phases remaining?                           │
│         → If YES: Continue to Step 4                             │
│         → If NO: Proceed to finish-branch                        │
│                                                                   │
│ Step 4: RE-READ THIS SKILL ← 🔴 CRITICAL!                        │
│         → Read skills/phase-protocol/SKILL.md again              │
│         → This refreshes context for next phase                  │
│                                                                   │
│ Step 5: CREATE NEXT PHASE TODO                                   │
│         → Follow Entry Protocol for Phase N+1                    │
│         → Start from Step 2 (tasks.md already known)             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase Transition Announcement

**When completing a phase and moving to next, announce:**

```markdown
---
## Phase N Complete ✅

**Completed tasks:**
- [x] Task 1
- [x] Task 2
- [x] Task 3

**Commit:** [sha] - [message]

**Documents updated:**
- tasks.md: Phase N tasks marked complete
- Completion Tracking: [X]% → [Y]%

---

## Transitioning to Phase N+1

Re-reading phase-protocol skill to refresh context...

[Then execute Entry Protocol for Phase N+1]
---
```

---

## Why This Works

```
┌────────────────────────────────────────────────────────────────┐
│ CONTEXT DRIFT PREVENTION MECHANISM                              │
├────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Problem: As conversation grows, AI forgets earlier context     │
│                                                                  │
│  Solution:                                                       │
│                                                                  │
│  1. TODO survives compression                                    │
│     → Created early, stays visible throughout phase             │
│                                                                  │
│  2. Exit Gate forces re-read                                     │
│     → Last TODO item: "Re-read protocol + Create next TODO"     │
│     → Cannot complete without reading this skill again          │
│                                                                  │
│  3. Entry Gate rebuilds context                                  │
│     → Re-reading docs rebuilds understanding                    │
│     → Gate verification ensures nothing skipped                 │
│                                                                  │
│  4. Loop continues automatically                                 │
│     → Exit → Re-read → Entry → Exit → Re-read → ...             │
│                                                                  │
│                                                                  │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐                       │
│  │Entry│───▶│Tasks│───▶│Exit │───▶│Entry│───▶ ...               │
│  │Gate │    │     │    │Gate │    │Gate │                       │
│  └─────┘    └─────┘    └──┬──┘    └─────┘                       │
│                           │          ▲                           │
│                           │          │                           │
│                           └──────────┘                           │
│                         Re-read skill                            │
│                                                                  │
└────────────────────────────────────────────────────────────────┘
```

---

## Common Mistakes to Avoid

| Mistake | Consequence | Correct Action |
|---------|-------------|----------------|
| Read docs before creating TODO | TODO incomplete after compression | Create TODO at Step 3, BEFORE reading docs |
| Skip Gate-4 verification | Missing items discovered too late | Always output completeness check |
| Skip Gate-8 understanding | Start coding without clear goal | Always output key understanding |
| Forget Exit-3 (re-read skill) | Context lost, next phase starts blind | Exit-3 is NON-NEGOTIABLE |
| Combine multiple phases | Exit Gate skipped, context drifts | One phase at a time |
| Mark TODO done without doing | Gate verification fails | Actually complete each item |

---

## Integration with execute skill

This skill is invoked by `superspec:execute` (subagent-development):

1. At execution start → Read this skill
2. Before each phase → Re-read this skill
3. After each phase → Exit Gate forces re-read

**The execute skill should NOT duplicate this protocol. It should reference it.**

---

## Quick Reference

```
ENTRY: Read skill → Read tasks → CREATE TODO → Gate → Read docs → Gate → Implement
EXIT:  Update tasks → Commit → Re-read skill → Create next TODO → Loop back
```

**The most important rule:** Create TODO BEFORE reading other documents.
