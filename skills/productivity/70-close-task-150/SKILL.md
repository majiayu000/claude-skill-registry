---
name: 70-close-task-150
description: "[70] CLOSE. Manage task lifecycle with correct statuses and no duplicates. Ensure each task has one status, artifacts match claims, and no task appears in multiple places. Use when managing task lists, updating progress, or ensuring task tracking integrity across systems."
---

# Close-Task 150 Protocol

**Core Principle:** One task, one status, one location. Status matches reality. Artifacts prove completion. No duplicates anywhere.

## What This Skill Does

When you invoke this skill, you're asking AI to:
- **Track status accurately** — Status reflects real state
- **Align artifacts** — Deliverables match status claims
- **Prevent duplicates** — No task in multiple places
- **Enforce lifecycle** — Proper state progression
- **Maintain integrity** — Cross-system consistency

## The 150% Tracking Rule

| Dimension | 100% Core | +50% Enhancement |
|-----------|-----------|------------------|
| **Status** | Correct state | + Transition reason documented |
| **Artifacts** | Match status | + Quality verified |
| **Duplicates** | None found | + Cross-system check |
| **Audit** | Changes logged | + Full history preserved |

## Task Lifecycle States

```
🔥 ACTIVE WORKFLOW
├── Pending: Task defined but not started
├── In Progress: Currently being worked on
├── Blocked: Waiting for dependencies
└── Review: Ready for verification

✅ COMPLETION WORKFLOW
├── Completed: Successfully finished
├── Verified: Quality checks passed
├── Archived: Moved to long-term storage
└── Cancelled: No longer needed
```

## State Transition Rules

```
Valid Transitions:

Pending → In Progress (work started)
Pending → Cancelled (no longer needed)

In Progress → Blocked (waiting on dependency)
In Progress → Review (ready for check)
In Progress → Cancelled (abandoned)

Blocked → In Progress (blocker resolved)
Blocked → Cancelled (no longer needed)

Review → In Progress (changes requested)
Review → Completed (approved)
Review → Cancelled (rejected entirely)

Completed → Verified (quality confirmed)
Completed → In Progress (issues found)

Verified → Archived (stored long-term)
```

## When to Use This Skill

- **Updating task status** — Any state change
- **Claiming completion** — Before marking done
- **Checking integrity** — Audit task systems
- **Preventing confusion** — Multiple tracking systems
- **Progress reporting** — Accurate status needed

## Execution Protocol

### Step 1: CURRENT STATE VERIFICATION
```
📋 **TASK STATE CHECK**

**Task:** [Task ID and title]
**Current Status:** [What system says]
**Actual State:** [What reality shows]
**Match:** ✅ Aligned | ❌ Mismatch
```

### Step 2: ARTIFACT VALIDATION
```
📦 **ARTIFACT CHECK**

**Status Claimed:** [e.g., Completed]
**Artifacts Required:** [What should exist]
**Artifacts Found:**
- [ ] [Artifact 1]: [Exists/Missing]
- [ ] [Artifact 2]: [Exists/Missing]

**Alignment:** ✅ Match | ❌ Gap
```

### Step 3: DUPLICATE CHECK
```
🔍 **DUPLICATE SCAN**

**Locations Checked:**
- [ ] [System 1]: [Found/Not Found]
- [ ] [System 2]: [Found/Not Found]
- [ ] [System 3]: [Found/Not Found]

**Duplicates Found:** [None / List them]
**Action Required:** [None / Consolidate]
```

### Step 4: STATUS TRANSITION
```
🔄 **STATUS UPDATE**

**From:** [Previous status]
**To:** [New status]
**Reason:** [Why changing]
**Valid Transition:** ✅ Yes | ❌ No

**Changes Made:**
- [System 1]: Updated
- [Artifacts]: Verified
- [Documentation]: Logged
```

### Step 5: INTEGRITY CONFIRMATION
```
✅ **INTEGRITY VERIFIED**

**Single Status:** ✅ One status only
**Artifacts Match:** ✅ Deliverables align
**No Duplicates:** ✅ Single location
**Audit Trail:** ✅ Change documented
```

## Output Format

For status updates:
```
📋 **TASK-TRACK 150 UPDATE**

**Task:** [ID] — [Title]

**Status Change:**
├── From: [Previous]
├── To: [New]
└── Reason: [Why]

**Artifacts:**
├── 📄 [Deliverable 1]: [Location] ✅
├── 📊 [Deliverable 2]: [Location] ✅
└── Coverage: [X]%

**Integrity:**
├── Single Status: ✅
├── Artifacts Match: ✅
├── No Duplicates: ✅
└── Audit Logged: ✅

**Confirmation Required?** [Yes/No]
```

For integrity audits:
```
🔍 **TASK-TRACK 150 AUDIT**

**Scope:** [What was checked]

**Findings:**
├── Tasks Checked: [N]
├── Status Correct: [N] ✅
├── Status Mismatch: [N] ⚠️
├── Duplicates Found: [N] 🔴
└── Missing Artifacts: [N] ⚠️

**Issues:**
1. [Task X]: [Problem] → [Fix]
2. [Task Y]: [Problem] → [Fix]

**Actions Taken:**
- [Action 1]
- [Action 2]

**System Integrity:** [✅ Clean | ⚠️ Issues Fixed | 🔴 Needs Attention]
```

## Task Status Format

```
🔥 **[ID] — [Task Title]**

**Status:** [Current State] | **Priority:** [Level]
**Created:** [Date] | **Due:** [Date]

**Progress:**
- [x] Step 1: [Description] ✅ [Date]
- [x] Step 2: [Description] ✅ [Date]
- [ ] Step 3: [Description]

**Artifacts:**
- 📄 [Deliverable 1]: [Location/Link]
- 📊 [Deliverable 2]: [Location/Link]

**Blockers:** [None / List]
**Notes:** [Updates, context, next steps]
```

## Operational Rules

1. **STATUS ACCURACY:** Status always reflects reality
2. **ARTIFACT ALIGNMENT:** Deliverables must match status
3. **DUPLICATE PREVENTION:** Strict control, one location only
4. **LIFECYCLE ENFORCEMENT:** Follow valid transitions
5. **DOCUMENTATION:** Log all status changes with reasons
6. **CROSS-SYSTEM SYNC:** Consistent across all systems

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Duplicate Tasks** | Same task in multiple places | Consolidate, remove duplicates |
| **Status Mismatch** | Status doesn't match artifacts | Correct status or complete work |
| **Lifecycle Violation** | Invalid state transition | Return to correct state |
| **Missing Audit** | No change documentation | Document all changes now |

## Examples

### ❌ Without Task-Track
```
Task UT-015:
- In "Active" section: "In Progress"
- In "Completed" section: "Done"
- In sprint board: "Review"

Result: Confusion, task worked on twice, wasted effort
```

### ✅ With Task-Track 150
```
📋 TASK-TRACK 150 UPDATE

Task: UT-015 — Implement user authentication

Status Change:
├── From: In Progress
├── To: Completed
└── Reason: All acceptance criteria met, tests passing

Artifacts:
├── 📄 auth.service.ts: /src/services/ ✅
├── 📊 auth.test.ts: /tests/ ✅ (94% coverage)
├── 📝 API docs: /docs/auth.md ✅
└── Coverage: 100%

Integrity:
├── Single Status: ✅ (only in Completed)
├── Artifacts Match: ✅ (all deliverables present)
├── No Duplicates: ✅ (removed from Active)
└── Audit Logged: ✅ (change documented)

Status: ✅ Verified
```

## Relationship to Other Skills

- **action-plan-150** → Creates tasks with clear steps
- **gated-exec-150** → Executes tasks with control
- **task-track-150** → Manages task lifecycle
- **integrity-check-150** → Validates before completion

---

**Remember:** Task tracking isn't bureaucracy — it's clarity. One status, one location, artifacts that prove completion. When everyone knows the real state, work flows smoothly.

