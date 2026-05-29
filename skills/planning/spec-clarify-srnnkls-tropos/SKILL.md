---
name: spec-clarify
description: Resolve ambiguities and markers in validation.yaml interactively. Updates spec docs directly with full audit trail.
---

# Spec Clarify Skill

Resolve ambiguities and markers by updating spec documents directly with tracked changes.

---

## When to Use

**Use for:**
- Resolving markers before task-dispatch (especially for Initiatives)
- Clarifying ambiguous requirements discovered post-validation
- Addressing gaps identified in ambiguity_scan

**Don't use for:**
- Initial validation (use spec-validate)
- Changing fundamental scope (re-run spec-validate)

---

## Workflow

### Step 1: Load and Scan

1. Find active spec in `./specs/active/*/`
2. Read `validation.yaml` from spec directory
3. Run ambiguity scan:
   - Check `ambiguity_scan` section for areas with `status: partial` or `status: missing`
   - These become clarification candidates alongside open markers
4. Collect open markers where `status: open`
5. Merge candidates: ambiguity gaps + open markers (deduplicate by area)
6. If no candidates: report "No unresolved items" and exit

### Step 2: Present Candidates

For each candidate (prioritized by impact), use AskUserQuestion:

```
Header: ${AREA}
Question: ${DESCRIPTION}
multiSelect: false
Options:
- [Generated options based on context]
- Defer: Skip for now
```

**Prioritization:** Scope > Behavior > Data Model > Constraints > Edge Cases > Integration > Terminology

### Step 3: Update Spec Documents Directly

When a clarification is resolved, update the relevant section in the source document:

| Clarification Area | Target Document | Target Section |
|--------------------|-----------------|----------------|
| Scope | spec.md | Requirements, Scope |
| Behavior | spec.md | Requirements, Behavior |
| Data Model | context.md | Data Model |
| Constraints | spec.md | Constraints |
| Edge Cases | spec.md | Edge Cases |
| Integration | context.md | Integration Points |
| Terminology | context.md | Terminology |

**Update approach:**
1. Read the target section
2. Integrate the clarification naturally into existing content
3. Do NOT create a separate "## Clarifications" section

### Step 4: Record Clarification Session

Create a new session entry in `clarification_sessions`:

```yaml
clarification_sessions:
  - id: S00${N}
    timestamp: ${ISO_TIMESTAMP}
    questions:
      - id: Q001
        question: "${QUESTION}"
        answer: "${ANSWER}"
        area: ${TAXONOMY_AREA}
        doc_updates:
          - file: spec.md
            section: Requirements
            action: modified
```

**doc_updates** tracks exactly which files/sections changed for audit trail.

### Step 5: Update Ambiguity Scan Status

For each resolved clarification from ambiguity gaps:

1. Update `ambiguity_scan.${area}.status` to `clear`
2. Remove the resolved gap from `ambiguity_scan.${area}.gaps`

### Step 6: Update Markers

For each resolved marker:

1. Change `status: open` to `status: resolved`
2. Add `resolution: "${USER_ANSWER}"`

### Step 7: Re-check Gates (Initiatives Only)

For Initiative specs:

1. Re-evaluate gates in validation.yaml
2. Update gate status if resolution changes assessment
3. Report gate status

---

## Doc Update Mapping

| Source | Target File | Target Section |
|--------|-------------|----------------|
| Scope gap | spec.md | ## Requirements or ## Scope |
| Behavior gap | spec.md | ## Requirements / Behavior subsection |
| Data Model gap | context.md | ## Data Model |
| Constraints gap | spec.md | ## Constraints |
| Edge Cases gap | spec.md | ## Edge Cases |
| Integration gap | context.md | ## Integration Points |
| Terminology gap | context.md | ## Terminology |

---

## Example Session

```
[Load validation.yaml]
[Run ambiguity scan]
- scope: partial (1 gap)
- data_model: missing (2 gaps)
[Check markers]
- M001 (Constraints): open

Candidates:
1. Scope: "User role boundaries unclear"
2. Data Model: "Schema for notifications not defined"
3. Data Model: "Retention policy not specified"
4. Constraints: "Authentication method not specified"

---
Header: Scope
Question: What user roles exist and what are their boundaries?

Options:
- Admin/User: Two-tier with admin full access
- Role-based: Granular permissions per feature
- Defer: Skip for now

User selects: Admin/User

[Update spec.md#requirements]
Added: "Two-tier role system: Admin (full access), User (standard permissions)"

[Record session]
clarification_sessions:
  - id: S001
    timestamp: 2025-01-15T10:30:00Z
    questions:
      - id: Q001
        question: "What user roles exist and what are their boundaries?"
        answer: "Two-tier: Admin (full access), User (standard permissions)"
        area: scope
        doc_updates:
          - file: spec.md
            section: Requirements
            action: modified

[Update ambiguity_scan]
scope:
  status: clear
  gaps: []

---
Header: Constraints
Question: Which authentication method should be used?
...
```

---

## Integration

**Invoked by:** `/spec.clarify` command

**Related skills:**
- `spec-validate` - Initial validation (creates ambiguity_scan and markers)
- `spec-create` - Document creation (references markers)
- `task-dispatch` - Checks for blocking markers before dispatch
