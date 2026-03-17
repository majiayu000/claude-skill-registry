---
name: aget-record-lesson
description: Record lessons learned from sessions as persistent, searchable, committable artifacts. Classifies each lesson as Framework (help other AGETs) or Domain (help principal).
version: 1.0.0
---

# /aget-record-lesson

Record lessons learned as structured L-docs in the git repo. Each lesson is classified to determine storage location and ID scheme.

## Purpose

Capture learnings in a persistent, searchable format that survives context windows and session boundaries. Enables knowledge accumulation across sessions.

## Input

$ARGUMENTS - Optional lesson description or trigger context

## Execution

### Step 1: Gather Context

Identify what triggered the lesson:
- Session observation
- User feedback
- Error encountered
- Pattern discovered
- Process improvement

### Step 2: Classify the Lesson

Ask the user:

> **Classification Required**
>
> Would this lesson help another AGET (different principal, different domain)?
>
> - **Framework** → Reusable across AGETs → `.aget/evolution/L###_*.md`
> - **Domain** → Helps this principal → `knowledge/patterns/*.md`

**Decision Tree**:
```
Would this help another AGET?
├── YES → Framework → .aget/evolution/L###_{name}.md (gets L-number)
└── NO  → Would this help the principal without an AGET?
    ├── YES → Domain → knowledge/patterns/{category}/{name}.md
    └── UNCLEAR → Ask user to clarify
```

### Step 3: Get Next ID (Framework only)

```bash
# Read next_id from index.json
jq '.next_id' .aget/evolution/index.json
```

### Step 4: Create Lesson Document

**Framework Template** (`.aget/evolution/L{ID}_{name}.md`):

```markdown
# L{ID}: {Title}

**Date**: {YYYY-MM-DD}
**Type**: Lesson Learned
**Category**: {category}
**Status**: complete

---

## Summary

{One paragraph summary of the lesson}

---

## Context

{What triggered this lesson? What were you doing?}

---

## Key Finding

{The core insight or learning}

---

## Implications

{What should change as a result?}

---

## Traceability

| Link | Reference |
|------|-----------|
| Session | {session file if applicable} |
| Project | {project plan if applicable} |
| Trigger | {what prompted this lesson} |

---

*L{ID}: {Title}*
*Category: {category}*
```

**Domain Template** (`knowledge/patterns/{category}/{name}.md`):

```markdown
# {Title}

**Created**: {YYYY-MM-DD}
**Category**: {category}
**Type**: Domain Knowledge

---

## Summary

{Description}

---

## Details

{Full content}

---
```

### Step 5: Update Index (Framework only)

Add entry to `.aget/evolution/index.json` and increment `next_id`.

### Step 6: Confirm

Report:
- File created at: {path}
- Classification: {Framework/Domain}
- ID: {L### or N/A}

## Constraints

- **C1**: MUST classify before writing. Do not proceed without Framework/Domain decision.
- **C2**: Framework lessons get L-numbers; Domain lessons do not.
- **C3**: Always update index.json for Framework lessons.
- **C4**: Never auto-classify. User must confirm classification.

## Classification Guidance

| Lesson Type | Classification | Example |
|-------------|---------------|---------|
| Process improvement for AGET framework | Framework | "Threshold calibration methodology" |
| Domain-specific knowledge | Domain | "Legalon contract parsing rules" |
| CLI behavior finding | Framework | "Skills work in headless mode" |
| Project-specific pattern | Domain | "API rate limit handling" |
| Anti-pattern applicable to all AGETs | Framework | "Context-Anchoring Blindness" |

## Related Skills

- `/aget-healthcheck-evolution` - Check evolution directory health
- `/aget-capture-observation` - Capture observations (lighter weight)

## Traceability

| Link | Reference |
|------|-----------|
| POC | POC-017 |
| Project | PROJECT_PLAN_AGET_UNIVERSAL_SKILLS.md |
| Source | Fleet Skill Deployment Report (supervisor) |

---

*aget-record-lesson v1.0.0*
*Category: Learning*
*POC-017 Phase 2*
