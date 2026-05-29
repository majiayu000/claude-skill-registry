---
name: manage-references
description: Manage references.toon files with field-level access and list management
allowed-tools: Read, Glob, Bash
---

# Manage References Skill

Manage references.toon files with field-level access and list management. Tracks files, branches, and external references for a plan.

## What This Skill Provides

- Read/write references.toon
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
.plan/plans/{plan_id}/references.toon
```

---

## File Format

TOON format with scalar and list fields:

```toon
# Plan References

branch: feature/my-feature
issue_url: https://github.com/org/repo/issues/123
build_system: maven

modified_files[3]:
- src/main/java/Foo.java
- src/main/java/Bar.java
- src/test/java/FooTest.java

external_docs[1]{title,url}:
JWT Guide,https://jwt.io/introduction
```

### Schema Fields

| Field | Type | Description |
|-------|------|-------------|
| `branch` | string | Git branch name |
| `issue_url` | string | GitHub issue URL |
| `build_system` | string | Build system (maven, gradle, npm, none) |
| `modified_files` | list | Files modified during implementation |
| `config_files` | list | Configuration files changed |
| `test_files` | list | Test files created/modified |
| `external_docs` | table | External documentation references |

---

## Operations

Script: `pm-workflow:manage-references:manage-references`

### create

Create references.toon with basic fields.

```bash
python3 .plan/execute-script.py pm-workflow:manage-references:manage-references create \
  --plan-id {plan_id} \
  --branch {branch_name} \
  [--issue-url {url}] \
  [--build-system {maven|gradle|npm}]
```

**Parameters**:
- `--plan-id` (required): Plan identifier (kebab-case)
- `--branch` (required): Git branch name
- `--issue-url`: GitHub issue URL
- `--build-system`: Build system (`maven`, `gradle`, `npm`)

**Output** (TOON):
```toon
status: success
plan_id: my-feature
file: references.toon
created: true
fields:
  - branch
  - base_branch
  - modified_files
  - config_files
  - test_files
```

**Note**: Basic fields are created during plan-init. Additional reference fields are added as needed during execution.

### read

Read entire references.toon content.

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
config_files_count: 1
test_files_count: 2
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
config_files_count: 1
test_files_count: 2
modified_files:
  - src/main/java/Foo.java
  - src/main/java/Bar.java
  - src/main/java/Baz.java
config_files:
  - pom.xml
test_files:
  - src/test/java/FooTest.java
  - src/test/java/BarTest.java
```

---

## Scripts

**Script**: `pm-workflow:manage-references:manage-references`

| Command | Parameters | Description |
|---------|------------|-------------|
| `create` | `--plan-id --branch [--issue-url] [--build-system]` | Create references.toon |
| `read` | `--plan-id` | Read entire references |
| `get` | `--plan-id --field` | Get specific field value |
| `set` | `--plan-id --field --value` | Set specific field value |
| `add-file` | `--plan-id --file` | Add file to modified_files |
| `remove-file` | `--plan-id --file` | Remove file from modified_files |
| `get-context` | `--plan-id [--include-files]` | Get all references context |

---

## Error Handling

```toon
status: error
plan_id: my-feature
error: file_not_found
message: references.toon not found
```

---

## Integration Points

### With plan-execute

Execution phase adds modified files as work progresses.

### With plan-finalize

Finalization reads modified files for commit/PR creation.
