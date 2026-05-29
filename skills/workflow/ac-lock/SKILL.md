---
name: ac-lock
description: Phase 4.0 — Acceptance Criteria lock checkpoint before implementation. Consolidates all ACs from PRD, TechSpec, and Tasks, presents to user for confirmation, and saves the locked AC list to accepted-criteria.md. Implementation only starts after explicit user confirmation.
---

# AC Lock Checkpoint

Runs **automatically as Phase 4.0**, after Tasks Validation and before the first implementation task.
Purpose: give the user one final explicit confirmation that the Acceptance Criteria represent what they actually want — before any implementation begins.

## Position in flow

```
[Tasks Validation]
      ↓
[AC Lock Checkpoint]  ← THIS SKILL
      ↓
Per-Task: implementation
```

## Entry conditions

- `prd.md`, `techspec.md`, and `tasks.md` must exist in `tasks/prd-{slug}/`
- Generates `accepted-criteria.md` in `.claude/feature-state/{slug}/`
- If `accepted-criteria.md` already exists (resume case): skip extraction, ask user to confirm current locked ACs or unlock to re-confirm
- Implementation **must not start** until this file is saved

---

## Step 1: Extract and Consolidate ACs

### Sources

Read ACs from all three documents:

**From `prd.md`:**
- "Goals" or "Objectives" section (functional success criteria)
- "Acceptance Criteria" section (if present)
- "Success Metrics" section (if present)

**From `techspec.md`:**
- "Validation & Testing Plan" section
- "Acceptance Criteria" section (if present)
- Non-functional requirements that can be verified

**From `tasks.md`:**
- "Acceptance Criteria" or "Done When" column/field per task
- Any inline criteria in task descriptions

### Deduplication

Merge near-duplicate ACs (same intent, slightly different wording):
- "trainerId is saved to Firestore" + "trainerId is persisted on student document" → consolidate as one
- Use the more specific/verifiable version

### Classification

Group ACs into three categories:

1. **Functional** — observable user/system behavior
   - e.g., "Trainer can see their connected students in /cms/students"

2. **Technical** — implementation-level verifiable criteria
   - e.g., "POST /api/students saves trainerId field"
   - e.g., "Firestore security rules validated"

3. **Quality** — non-functional, cross-cutting
   - e.g., "All use cases have unit tests"
   - e.g., "No breaking changes to existing API consumers"

---

## Step 2: Present to User

Present the consolidated list with clear formatting before any implementation starts:

```
✋ AC Lock Checkpoint — Confirm Before Implementation

This feature will be considered DONE when all of the following are true:

**Functional**
1. [ ] Personal trainer can see all linked students in /cms/students
2. [ ] Student appears in trainer's list after successful Firestore connection
3. [ ] trainerId is persisted on student document in Firestore

**Technical**
4. [ ] POST /api/students saves trainerId field from auth context
5. [ ] GET /api/students filters by authenticated trainer's uid
6. [ ] Firestore security rules allow trainer to read their students only

**Quality**
7. [ ] All new use cases have unit tests
8. [ ] No breaking changes to existing /api/students consumers

---

Does this accurately capture what you want?

  yes           → Lock these ACs and start implementation
  adjust N      → Edit AC number N (e.g., "adjust 3")
  add           → Add a missing AC
  remove N      → Remove AC number N
  show-sources  → Show which document each AC came from
```

---

## Step 3: Interactive Adjustment

Allow the user to modify the AC list before locking:

### "adjust N" — edit one AC

```
Current AC-3: "trainerId is persisted on student document in Firestore"
New AC-3: [user input]
```

Replace the AC in the list and re-present the relevant section.

### "add" — add a missing AC

```
Enter new AC (describe what must be true when the feature is done):
[user input]

Category: functional / technical / quality?
```

Append to the appropriate category.

### "remove N" — remove an AC

```
Removing AC-5: "GET /api/students filters by authenticated trainer's uid"
Are you sure? This requirement won't be tracked. (yes/no)
```

### "show-sources" — show provenance

```
AC-1 → prd.md: Goals section
AC-4 → techspec.md: Validation & Testing Plan
AC-7 → tasks.md: Task 6 - "Done When" criteria
```

---

## Step 4: Lock and Persist

After user confirms with `yes`:

Save to `.claude/feature-state/{slug}/accepted-criteria.md`:

```markdown
## Accepted Criteria — Locked

Feature: {slug}
Locked: {timestamp}
Locked by: user confirmation

> ⚠️ This file is immutable during implementation.
> Do not edit after locking.

### Functional
- [ ] AC-1: Personal trainer can see all linked students in /cms/students
- [ ] AC-2: Student appears in trainer's list after successful Firestore connection
- [ ] AC-3: trainerId is persisted on student document in Firestore

### Technical
- [ ] AC-4: POST /api/students saves trainerId field from auth context
- [ ] AC-5: GET /api/students filters by authenticated trainer's uid
- [ ] AC-6: Firestore security rules allow trainer to read their students only

### Quality
- [ ] AC-7: All new use cases have unit tests
- [ ] AC-8: No breaking changes to existing /api/students consumers

### Sources
| AC | Source |
|----|--------|
| AC-1 | prd.md: Goals |
| AC-4 | techspec.md: Validation & Testing Plan |
| AC-7 | tasks.md: Task 6 |
```

---

## Step 5: PR Coverage Verification

During Phase 5 (Commit & PR), read `accepted-criteria.md` and check which ACs are covered:

### Coverage check

For each AC, check if implementation tasks have been completed that address it:
- Match tasks marked ✅ in the task list against AC keywords
- Mark covered ACs as `[x]` in the coverage report

### PR description includes

```markdown
## Definition of Done

**Covered by this PR:**
- [x] AC-1: Personal trainer can see all linked students in /cms/students
- [x] AC-2: Student appears in trainer's list after Firestore connection
- [x] AC-4: POST /api/students saves trainerId field

**Known gaps (not covered):**
- [ ] AC-7: Unit tests — partial (3 of 5 use cases tested)

> Full AC list: .claude/feature-state/{slug}/accepted-criteria.md
```

If all ACs are covered → no "Known gaps" section.

---

## Behavior Summary

| State | Behavior |
|-------|----------|
| `accepted-criteria.md` does not exist | Run full AC Lock flow |
| File exists, `--resume` flag | Show locked ACs, ask to confirm or unlock |
| File exists, `--force-relock` flag | Re-run extraction, allow new confirmation |
| User skips (emergency) | Warn, log "AC Lock bypassed", proceed without file |

### Emergency bypass

If the user explicitly wants to skip AC Lock (e.g., rapid prototype):
```
⚠️ AC Lock bypassed — implementation will proceed without locked ACs.
   PR will not include a "Definition of Done" section.
   Type "skip-ac-lock" to confirm.
```

Log the bypass in `.claude/feature-state/{slug}/checkpoint.json`.
