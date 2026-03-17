---
name: ralph-add
description: Add new stories to an existing prd.json without resetting completed story statuses. Use this to extend a project with new features.
argument-hint: "<prd-file.md> | --inline"
---

## Purpose

Add new user stories to an existing `prd.json` while preserving the status of all completed stories. Use this when you want to extend a project with new features without losing progress.

## Arguments

- `<prd-file.md>` — Path to PRD markdown file containing ONLY the new stories to add
- `--inline` — Interactively define new stories (no file needed)

## Behavior

### What It Preserves

- All existing stories and their `passes` status
- Existing story IDs, priorities, and all fields
- Project name and description

### What It Does

1. **Reads existing** `scripts/ralph/prd.json`
2. **Parses new stories** from the provided PRD file or inline input
3. **Validates** no duplicate story IDs
4. **Assigns priorities** to new stories (starting after highest existing priority)
5. **Merges** new stories into the existing array
6. **Writes** updated prd.json

### Duplicate ID Handling

If a new story has an ID that already exists:
- **Warn** the user about the conflict
- **Skip** the duplicate story (do not overwrite)
- **Continue** with remaining new stories

---

## Workflow

### Option 1: From PRD File

```bash
/ralph-add docs/new-features.md
```

The PRD file should contain ONLY the new stories in standard PRD format:

```markdown
# New Features

## Feature: User Notifications
Users receive email notifications for important events.

### Acceptance Criteria
- Email sent on new message
- Email sent on mention
- Unsubscribe link in all emails

### Notes
Use SendGrid for email delivery.
```

### Option 2: Inline Definition

```bash
/ralph-add --inline
```

Then provide story details interactively or in the prompt.

---

## Priority Assignment

New stories receive priorities starting AFTER the highest existing priority:

**Before (existing prd.json):**
```json
{
  "userStories": [
    { "id": "setup-001", "priority": 1, "passes": true },
    { "id": "auth-001", "priority": 2, "passes": true },
    { "id": "crud-001", "priority": 3, "passes": false }
  ]
}
```

**After adding 2 new stories:**
```json
{
  "userStories": [
    { "id": "setup-001", "priority": 1, "passes": true },
    { "id": "auth-001", "priority": 2, "passes": true },
    { "id": "crud-001", "priority": 3, "passes": false },
    { "id": "notif-001", "priority": 4, "passes": false },
    { "id": "export-001", "priority": 5, "passes": false }
  ]
}
```

---

## Story ID Convention

Generate IDs following existing patterns in the project:

| Pattern | Examples |
|---------|----------|
| `{category}-{number}` | `auth-001`, `crud-002`, `ui-003` |
| `{feature}-{number}` | `notif-001`, `export-001` |

Scan existing IDs to match the naming convention used in the project.

---

## Stack Detection

Follow the same stack detection rules as `/ralph`. Detect the project stack from the project root before assigning scaffold skills. See `/ralph` SKILL.md "Stack Detection" section for the indicator table.

## Scaffold Skill Auto-Detection

Apply the same rules as `/ralph` for auto-adding `scaffoldSkill`. Use the scaffold skill matching the detected stack:

| Story Type | MERN | NEAN | iOS |
|------------|------|------|-----|
| New CRUD feature | `mern-add-feature` | `nean-add-feature` | `ios-add-feature` |
| Authentication | `mern-add-auth` | `nean-add-auth` | `ios-add-auth` |
| Bug fix / Refactor / Config | (none) | (none) | (none) |

**Do NOT add scaffoldSkill for:**
- Bug fixes
- Refactoring
- Configuration/setup
- Static content
- UI-only changes
- Extending existing features

---

## prd.json Story Schema

New stories must follow this schema:

```json
{
  "id": "string (kebab-case, e.g., notif-001)",
  "title": "string (short, imperative)",
  "priority": "number (auto-assigned)",
  "description": "string (what to implement)",
  "acceptanceCriteria": ["string (testable criteria)"],
  "testCriteria": ["string (specific test assertions)"],
  "testFiles": ["string (test file paths)"],
  "filesToCreate": ["string (expected file paths)"],
  "scaffoldSkill": "string (optional)",
  "notes": "string (optional)",
  "passes": false
}
```

**Note:** New stories always start with `passes: false`.

---

## Validation

Before writing, validate:

1. **prd.json exists** at `scripts/ralph/prd.json`
2. **No duplicate IDs** between existing and new stories
3. **Required fields** present for each new story (id, title, description, acceptanceCriteria)
4. **testCriteria derived** from acceptanceCriteria (for TDD)
5. **testFiles specified** for each story

---

## Output

After successful merge:

```
Added 2 new stories to prd.json:

  notif-001: User Notifications (priority 4)
  export-001: Data Export (priority 5)

Existing stories preserved:
  - setup-001 (passes: true)
  - auth-001 (passes: true)
  - crud-001 (passes: false)

Total stories: 5 (2 completed, 3 pending)

Run ./scripts/ralph/ralph-once.sh to start the next story.
```

---

## Error Cases

| Error | Resolution |
|-------|------------|
| `prd.json not found` | Run `/ralph` first to set up the project |
| `Duplicate ID: auth-001` | Rename the new story ID or skip it |
| `Missing acceptance criteria` | Add criteria to the PRD file |
| `Invalid PRD format` | Check markdown structure |

---

## Examples

### Add features from a file

```bash
/ralph-add docs/phase-2-features.md
```

### Add a single story inline

```bash
/ralph-add --inline

# Then describe:
# "Add a notifications feature where users get email alerts for new messages"
```

### Check what would be added (dry run)

```bash
/ralph-add docs/new-features.md --dry-run
```

---

## Self-Improvement

After this skill completes, run `/retro-create` to review the session for issues
and improve this skill. This is automatic — do not skip it.

---

## Comparison with /ralph

| Aspect | `/ralph` | `/ralph-add` |
|--------|----------|--------------|
| Creates prd.json | Yes (from scratch) | No (must exist) |
| Preserves status | No (all reset to false) | Yes |
| Sets up scripts | Yes (with --setup) | No |
| Use case | New project | Extending existing project |
