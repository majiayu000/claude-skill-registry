---
name: manage-files
description: Generic file I/O operations for plan directories
user-invocable: false
allowed-tools: Read, Glob, Bash
---

# Manage Files Skill

Generic file operations for plan directories. Provides basic CRUD operations for any file within a plan directory.

## What This Skill Provides

- Generic file read/write/remove operations
- Directory listing and creation
- File existence checking
- Plan directory create-or-reference (atomic check/create)
- No content validation (caller provides complete content)

## When to Activate This Skill

Activate this skill when:
- Reading or writing arbitrary files in a plan directory
- Creating subdirectories within a plan
- Listing plan contents
- Checking if files exist

**Note**: For typed plan documents (`request.md`, `solution_outline.md`), use `pm-workflow:manage-plan-documents` instead. For domain-specific files (references.json, status.toon), use the dedicated manage-* skills.

---

## Storage Location

Files are stored in plan directories:

```
.plan/plans/{plan_id}/
  request.md
  solution_outline.md
  references.json
  status.toon
  tasks/
```

---

## Operations

Script: `pm-workflow:manage-files:manage-files`

### read

Read file content from a plan directory.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files read \
  --plan-id {plan_id} \
  --file notes.md
```

**Output**: Raw file content (no wrapping)

### write

Write content to a file in a plan directory.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files write \
  --plan-id {plan_id} \
  --file request.md \
  --content "# Request Title

Task description with multiline content.

## Section

More content here..."
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--file` (required): Relative file path within plan directory
- `--content`: Content to write (mutually exclusive with `--stdin`)
- `--stdin`: Read content from stdin instead of `--content`

**Note**: The `--content` parameter supports multiline content. Do NOT use `--stdin` with shell heredocs or cat commands.

**Output**: Prints "Created: {path}" to stderr, exit code 0 on success

### remove

Remove a file from a plan directory.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files remove \
  --plan-id {plan_id} \
  --file old-file.md
```

**Output**: Confirmation message to stderr, exit code 0 on success

### list

List files in a plan directory.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files list \
  --plan-id {plan_id} \
  [--dir subdir]
```

**Output**: Simple file listing, one per line

### exists

Check if a file exists. Returns TOON output with `exists: true/false`.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files exists \
  --plan-id {plan_id} \
  --file references.json
```

**Output** (TOON format):

When file exists:
```toon
status: success
plan_id: my-feature
file: references.json
exists: true
path: .plan/plans/my-feature/references.json
```

When file does not exist:
```toon
status: success
plan_id: my-feature
file: missing.md
exists: false
path: .plan/plans/my-feature/missing.md
```

On validation error (invalid plan_id or path):
```toon
status: error
plan_id: Invalid_Plan
error: invalid_plan_id
message: Invalid plan_id format: Invalid_Plan
```

**Note**: Always exits 0 for expected outcomes. Check `status` and `exists` fields to determine result

### mkdir

Create a subdirectory in a plan directory.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files mkdir \
  --plan-id {plan_id} \
  --dir requirements
```

**Output** (TOON format):

```toon
status: success
plan_id: my-feature
action: created
dir: requirements
path: /path/to/.plan/plans/my-feature/requirements
```

The `action` field is `created` if the directory was newly created, or `exists` if it already existed.

### create-or-reference

Create a plan directory if it doesn't exist, or reference an existing one. This is an atomic operation that replaces the two-step pattern of listing plans and checking for conflicts.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files create-or-reference \
  --plan-id {plan_id}
```

**Output** (TOON format):

When plan is newly created:
```toon
status: success
plan_id: my-feature
action: created
path: /path/to/.plan/plans/my-feature
```

When plan already exists:
```toon
status: success
plan_id: my-feature
action: exists
path: /path/to/.plan/plans/my-feature
current_phase: refine
domain: java
```

**Use case**: Called by plan-init to atomically check/create plan directories.

### delete-plan

Delete an entire plan directory. Used when user selects "Replace" for an existing plan during plan-init.

```bash
python3 .plan/execute-script.py pm-workflow:manage-files:manage-files delete-plan \
  --plan-id {plan_id}
```

**Output** (TOON format):

On success:
```toon
status: success
plan_id: my-feature
action: deleted
path: /path/to/.plan/plans/my-feature
files_removed: 5
```

On error (plan not found):
```toon
status: error
plan_id: my-feature
error: plan_not_found
message: Plan directory does not exist: /path/to/.plan/plans/my-feature
```

**Use case**: Called by plan-init when user selects "Replace" to delete existing plan before creating new one. See `pm-workflow:phase-1-init/standards/plan-overwrite.md` for the full workflow.

---

## Key Design Principles

1. **plan_id only** - Never pass full paths, script resolves base via `base_path()`
2. **Relative file paths** - `--file` accepts relative paths within plan dir (e.g., `requirements/REQ-001.toon`)
3. **Generic file operations** - Not domain-specific (no parse-plan, write-config)
4. **Plain output** - `read` returns raw content; mutations return minimal status
5. **No validation** - Caller provides complete content; no content validation

---

## Validation Rules

| Check | Validation |
|-------|------------|
| plan_id format | kebab-case, no special chars |
| file path | No `..`, no absolute paths |
| directory | Must exist (unless mkdir) |
| content | Non-empty for write |

---

## Error Handling

```toon
status: error
plan_id: my-feature
file: nonexistent.md
error: file_not_found
message: File does not exist

suggestions[2]:
- Check file name spelling
- Use list subcommand to see available files
```

---

## Integration Points

### With Domain Skills

Domain-specific skills (manage-references, manage-lifecycle) may use this skill for basic file operations, or import shared libraries directly.

### With Orchestration Skills

Plan orchestration skills (plan-init, solution-outline, task-plan, plan-execute) use this skill for generic file I/O.

---

## Relationship to Domain Skills

| Skill | Manages | Use manage-files for |
|-------|---------|---------------------|
| manage-references | references.json | N/A (use manage-references) |
| manage-lifecycle | status.toon | N/A (use manage-lifecycle) |
| manage-plan-documents | request.md | N/A (use manage-plan-documents) |
| manage-solution-outline | solution_outline.md | N/A (use manage-solution-outline) |
| manage-tasks | tasks/*.toon | N/A (use manage-tasks) |
| manage-files | any other file | Generic read/write/list |
