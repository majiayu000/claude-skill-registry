---
name: manage-references
description: Manage references.json files with field-level access and list management
user-invocable: false
allowed-tools: Read, Glob, Bash
---

# Manage References Skill

Manage references.json files with field-level access and list management. Tracks files, branches, and external references for a plan.

## What This Skill Provides

- Read/write references.json (JSON storage, TOON output)
- Field-level get/set operations
- List management (add/remove items)
- File tracking for modified files

## When to Activate This Skill

Activate this skill when:
- Setting branch or issue references
- Adding modified files to tracking
- Managing external documentation references

---

## Storage Location

References are stored in the plan directory:

```
.plan/plans/{plan_id}/references.json
```

---

## File Format

JSON format for storage:

```json
{
  "branch": "feature/my-feature",
  "base_branch": "main",
  "issue_url": "https://github.com/org/repo/issues/123",
  "build_system": "maven",
  "modified_files": [
    "src/main/java/Foo.java",
    "src/main/java/Bar.java",
    "src/test/java/FooTest.java"
  ],
  "domains": ["java"],
  "affected_files": [
    "src/main/java/Foo.java"
  ]
}
```

### Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `branch` | string | Git branch name |
| `base_branch` | string | Base branch for PR (e.g., main) |
| `issue_url` | string | GitHub issue URL |
| `build_system` | string | Build system (maven, gradle, npm, none) |
| `modified_files` | list | Files modified during implementation |
| `domains` | list | Plan domains (e.g., java, documentation) |
| `affected_files` | list | Files affected during outline phase (for execution tracking) |
| `external_docs` | table | External documentation references |

---

## Operations

Script: `pm-workflow:manage-references:manage-references`

### create

Create references.json with basic fields.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references create \
  --plan-id {plan_id} \
  --branch {branch_name} \
  [--issue-url {url}] \
  [--build-system {maven|gradle|npm}] \
  [--domains {java,documentation}]
```

**Parameters**:
- `--plan-id` (required): Plan identifier (kebab-case)
- `--branch` (required): Git branch name
- `--issue-url`: GitHub issue URL
- `--build-system`: Build system (`maven`, `gradle`, `npm`)
- `--domains`: Comma-separated domain list (e.g., `java,documentation`)

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: references.json
created: true
fields[3]:
  - branch
  - base_branch
  - modified_files
```

**Note**: Basic fields are created during plan-init. Additional reference fields are added as needed during execution.

### read

Read entire references.json content.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references read \
  --plan-id {plan_id}
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature

references:
  branch: feature/my-feature
  issue_url: https://github.com/org/repo/issues/123
  modified_files: 3 items
```

### get

Get a specific field value.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get \
  --plan-id {plan_id} \
  --field branch
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: branch
value: feature/my-feature
```

### set

Set a specific field value.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references set \
  --plan-id {plan_id} \
  --field branch \
  --value feature/new-branch
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: branch
value: feature/new-branch
previous: feature/my-feature
```

### add-file

Add a file to modified_files list.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references add-file \
  --plan-id {plan_id} \
  --file src/main/java/NewClass.java
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
section: modified_files
added: src/main/java/NewClass.java
total: 4
```

### remove-file

Remove a file from modified_files list.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references remove-file \
  --plan-id {plan_id} \
  --file src/main/java/OldClass.java
```

**Output** (TOON):
```toon
status: success
plan_id: my-feature
section: modified_files
removed: src/main/java/OldClass.java
total: 2
```

### add-list

Add multiple values to a list field.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references add-list \
  --plan-id {plan_id} \
  --field affected_files \
  --values "path/to/file1.md,path/to/file2.md,path/to/file3.md"
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--field` (required): List field name (e.g., `affected_files`, `modified_files`)
- `--values` (required): Comma-separated values to add

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: affected_files
added_count: 3
total: 3
```

**Notes**:
- Creates the field as an empty list if it doesn't exist
- Skips values that already exist in the list (no duplicates)
- Returns error if the field exists but is not a list

### set-list

Set a list field to new values, replacing any existing content.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references set-list \
  --plan-id {plan_id} \
  --field affected_files \
  --values "path/to/file1.md,path/to/file2.md"
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--field` (required): List field name (e.g., `affected_files`, `modified_files`)
- `--values` (required): Comma-separated values

**Output** (TOON):
```toon
status: success
plan_id: my-feature
field: affected_files
previous_count: 5
count: 2
```

**Notes**:
- Replaces the entire list (does not append like `add-list`)
- Empty `--values ""` clears the list
- Returns `previous_count` showing how many items were replaced

**When to use `set-list` vs `add-list`**:
- Use `set-list` when you have the complete list of values to store
- Use `add-list` when appending to an existing list without knowing its contents

### get-context

Get all references context in one call. Useful for getting comprehensive plan context.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references get-context \
  --plan-id {plan_id} \
  [--include-files]
```

**Parameters**:
- `--plan-id` (required): Plan identifier
- `--include-files`: Include full file lists in output (default: only counts)

**Output** (TOON):
```toon
status: success
plan_id: my-feature
branch: feature/my-feature
base_branch: main
modified_files_count: 3
issue_url: https://github.com/org/repo/issues/123
build_system: maven
```

With `--include-files`:
```toon
status: success
plan_id: my-feature
branch: feature/my-feature
base_branch: main
modified_files_count: 3
modified_files[3]:
  - src/main/java/Foo.java
  - src/main/java/Bar.java
  - src/main/java/Baz.java
```

---

## Scripts

**Script**: `pm-workflow:manage-references:manage-references`

| Command | Parameters | Description |
|---------|------------|-------------|
| `create` | `--plan-id --branch [--issue-url] [--build-system] [--domains]` | Create references.json |
| `read` | `--plan-id` | Read entire references |
| `get` | `--plan-id --field` | Get specific field value |
| `set` | `--plan-id --field --value` | Set specific field value |
| `add-file` | `--plan-id --file` | Add file to modified_files |
| `remove-file` | `--plan-id --file` | Remove file from modified_files |
| `add-list` | `--plan-id --field --values` | Add multiple values to a list field |
| `set-list` | `--plan-id --field --values` | Set a list field (replaces existing) |
| `get-context` | `--plan-id [--include-files]` | Get all references context |

---

## Error Handling

```toon
status: error
plan_id: my-feature
error: file_not_found
message: references.json not found
```

---

## Integration Points

### With plan-execute

Execution phase adds modified files as work progresses.

### With plan-finalize

Finalization reads modified files for commit/PR creation.
