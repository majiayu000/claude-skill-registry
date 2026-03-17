---
name: spec-archive
description: Archive completed development specs from ./specs/active/ to ./specs/archive/, updating documents with completion status and maintaining archive index. Use when finishing tasks or moving completed work to archive.
---

# Spec Archive Skill

Archive completed development specs with proper documentation and index maintenance.

> **Reference**: See [reference.md](reference.md).

---

## When to Use

Archive a spec when:
- All success criteria met
- Tests passing and code merged
- Ready to start new work
- Spec is "done enough" and blocking new work
- User explicitly requests archival

Don't archive when:
- Spec is actively in progress
- Blocking issues remain unresolved
- Branch has unmerged changes
- Critical checklist items incomplete (unless user confirms)

---

## Workflow

### Step 1: Validate Spec Argument

Parse spec name from command argument:

```bash
# User provides: add-temporal-joins
# Look for: ./specs/active/add-temporal-joins/
```

If not found, list available specs and ask which to archive.

### Step 2: Verify Completion Status

Before archiving, check:
- Read `spec.md` - status should be "Complete"
- Read `tasks.yaml` - verify all tasks have `status: completed`
- If incomplete, ask: "This spec appears incomplete. Archive anyway? (y/n)"

### Step 3: Pre-Archive Updates

Update documents before moving:

**In `spec.md`:**
- Set status to `Complete`
- Add `**Completed**: [Today's date]` after Started date
- Ensure all success criteria marked complete

**In `tasks.yaml`:**
- Update `meta.progress` to final count (e.g., "45/45")
- Update `meta.last_updated` to today
- Ensure all tasks have `status: completed`
- Mark any phase checkpoints as `verified: true`

**In `context.md`:**
- Update "Last Updated" to today
- Add Archive Notes section using [templates/archive-notes.md](templates/archive-notes.md)

### Step 4: Archive the Spec

```bash
mkdir -p ./specs/archive/
mv ./specs/active/{spec-name} ./specs/archive/{spec-name}
```

### Step 5: Git Operations (Optional)

If spec has associated branch:
1. Check current branch
2. If on spec branch, ask: "Switch back to main? (y/n)"
3. Ask: "Delete spec branch `{branch}` (only if merged)? (y/n)"

### Step 6: Create/Update Archive Index

Create `./specs/archive/README.md` if doesn't exist using [templates/archive-index.md](templates/archive-index.md).

Add entry at top of Archive Index section:

```markdown
### [Spec Name] - [Today's Date]
- **Duration**: [Started] → [Completed]
- **Branch**: [branch-name if applicable]
- **Summary**: [One sentence from spec.md Overview]
- **Location**: `./specs/archive/{spec-name}/`

---
```

### Step 7: Confirm Completion

Report to user:
```
Archived: {spec-name}

  From: ./specs/active/{spec-name}/
  To:   ./specs/archive/{spec-name}/

  Files archived:
  - spec.md (Complete)
  - context.md (Final notes added)
  - tasks.yaml (X/Y tasks complete)

  Archive index updated: ./specs/archive/README.md

  [If branch operations performed]:
  Git: Switched to main, deleted branch {branch}
```

---

## Partial Completion Handling

If archiving incomplete spec (user confirmed):
- Mark status as `Incomplete - [Reason]` not `Complete`
- In Archive Notes, clearly document what was NOT completed
- Explain why spec was abandoned/deferred
- Consider creating new spec for remaining work

---

## Archive Notes Template

See [templates/archive-notes.md](templates/archive-notes.md) for full template including:
- Summary (2-3 sentences)
- Key Outcomes (deliverables)
- Technical Debt / Future Work
- Lessons Learned

---

## Templates

- [templates/archive-notes.md](templates/archive-notes.md) - Archive Notes section for context.md
- [templates/archive-index.md](templates/archive-index.md) - Archive README template

---

## Success Criteria

- Spec moved from `./specs/active/` to `./specs/archive/`
- All three documents updated with completion status
- Archive Notes added to context.md
- Archive index entry created
- User informed of next steps

---

## Integration

**Workflow:**
- During task: Use `/spec.update` to sync status
- After task: Use this skill to archive
- Result: Clean `./specs/active/`, historical record preserved

**Related:**
- Command: `/spec.archive`
- Skills: `spec-create` (creation), `spec-update` (reminder)

---

## Reference

See [reference.md](reference.md) for archive organization guidelines and troubleshooting.
