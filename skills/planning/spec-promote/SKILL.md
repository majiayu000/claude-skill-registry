---
name: spec-promote
description: Promote spec from draft to active stage. Use after spec review passes or when ready to begin implementation.
---

# Spec Promote Skill

Promote validated specs from draft to active stage for implementation.

---

## When to Use

Promote a spec when:
- Spec validation passes (no open markers or user override)
- Ready to begin implementation
- Spec review approved
- User explicitly requests promotion

Don't promote when:
- Open markers exist without user override
- Initiative has failed gates
- Spec is incomplete or missing required documents
- Draft directory doesn't exist

---

## Workflow

### Step 1: Validate Spec Argument

Parse spec name from command argument:

```bash
# User provides: add-temporal-joins
# Look for: ./specs/draft/add-temporal-joins/
```

If not found, list available draft specs and ask which to promote.

### Step 2: Verify Readiness

Before promoting, check:

**Read `validation.yaml`** (if exists):
- Check markers section for `status: open`
- If open markers exist, warn user and ask to proceed anyway
- For Initiatives: check gates section for `status: failed`
- If failed gates exist, block promotion (require user to fix)

**Read `spec.md`**:
- Verify required sections exist
- Note current status for update

If validation.yaml doesn't exist (e.g., Task issue type), proceed without marker checks.

### Step 3: Move to Active

```bash
mkdir -p ./specs/active/
mv ./specs/draft/{spec-name} ./specs/active/{spec-name}
```

### Step 4: Update Metadata

Update `spec.md` frontmatter:

**Change:**
```yaml
status: Draft
stage: draft
```

**To:**
```yaml
status: Active
stage: active
promoted: {TODAY'S DATE}
```

If `stage` field doesn't exist, add it. Preserve all other frontmatter fields.

### Step 5: Report Success

Report to user:
```
Promoted: {spec-name}

  From: ./specs/draft/{spec-name}/
  To:   ./specs/active/{spec-name}/

  Status: Active
  Promoted: {DATE}

  [If open markers were overridden]:
  Warning: {N} open markers remain unresolved

Next steps:
  - Run /implement to begin task execution
  - Or use task-dispatch skill for parallel work
```

---

## Readiness Checks

### Marker Status Check

```yaml
# In validation.yaml
markers:
  - id: M001
    status: open    # WARN: ask user to proceed
  - id: M002
    status: resolved  # OK
```

Open markers indicate unresolved ambiguities. Warn but allow override.

### Gate Status Check (Initiatives Only)

```yaml
# In validation.yaml
gates:
  simplicity:
    status: failed  # BLOCK: cannot promote
  anti_abstraction:
    status: passed  # OK
```

Failed gates block promotion. User must resolve before promoting.

---

## Error Handling

| Condition | Action |
|-----------|--------|
| Spec not found in draft | List available drafts, ask user |
| Open markers | Warn, ask to proceed (y/n) |
| Failed gates | Block, explain which gates failed |
| Missing spec.md | Error: "Invalid spec directory" |
| Already in active | Error: "Spec already active" |

---

## Integration

**Workflow:**
- Create: `spec-validate` -> `spec-create` (creates in draft/)
- Review: Manual review or `/spec.clarify`
- Promote: This skill (draft/ -> active/)
- Execute: `task-dispatch` or `/implement`
- Archive: `spec-archive` (active/ -> archive/)

**Related:**
- Command: `/spec.promote`
- Skills: `spec-create` (creates drafts), `spec-archive` (archives active)
- Skill: `spec-clarify` (resolve open markers before promoting)
