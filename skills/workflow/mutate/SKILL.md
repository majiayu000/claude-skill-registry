---
name: mutate
description: Change persistent state with checkpoint and rollback support. Use when modifying files, updating databases, changing configuration, or any operation that permanently alters state.
argument-hint: "[target] [operation] [checkpoint_id]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Edit, Write, Bash
context: fork
agent: general-purpose
layer: EXECUTE
---

## Intent

Make controlled changes to persistent state with safety guarantees. This is the primary capability for modifications and REQUIRES a checkpoint for rollback capability.

**CRITICAL: This capability requires `checkpoint` to have been called first.**

**Success criteria:**
- State change applied correctly
- Previous state captured for rollback
- Change is verifiable
- Audit trail recorded

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `target` | Yes | string | What to modify (file path, resource identifier) |
| `operation` | Yes | object | The modification to apply |
| `checkpoint_id` | Yes | string | Checkpoint ID for rollback (from `checkpoint` capability) |

## Procedure

1) **Verify checkpoint exists**: Ensure recovery is possible
   - Confirm checkpoint_id references valid checkpoint
   - Verify checkpoint covers the target
   - STOP if no valid checkpoint

2) **Capture previous state**: Record what will change
   - Read current state of target
   - Store for comparison and rollback
   - Document what specifically will change

3) **Apply mutation**: Make the change
   - Execute the specified operation
   - Use appropriate tool (Edit for files, Bash for commands)
   - Capture any errors during modification

4) **Verify change**: Confirm mutation succeeded
   - Read new state
   - Compare to expected result
   - Note any unexpected side effects

5) **Record mutation**: Document what changed
   - Store diff between previous and new state
   - Record timestamp and operation details
   - Link to checkpoint for audit trail

6) **Return result**: Provide complete mutation record
   - Include success/failure status
   - Provide before/after state
   - Reference checkpoint for rollback

## Output Contract

Return a structured object:

```yaml
success: boolean  # Whether mutation completed
target: string  # What was modified
operation: string  # What was done
previous_state:
  snapshot: any  # State before mutation
  captured_at: string  # When captured
new_state:
  snapshot: any  # State after mutation
  verified_at: string  # When verified
diff:
  type: string  # unified, structural, summary
  content: string  # The actual diff
checkpoint_id: string  # For rollback reference
rollback_command: string  # How to undo this change
evidence_anchors: ["file:line", "command:output"]
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `success` | boolean | Whether mutation completed successfully |
| `target` | string | Resource that was modified |
| `operation` | string | Description of the change |
| `previous_state` | object | State before modification |
| `new_state` | object | State after modification |
| `diff` | object | Difference between states |
| `checkpoint_id` | string | Reference for rollback |
| `rollback_command` | string | How to undo the change |

## Examples

### Example 1: File Modification

**Input:**
```yaml
target: "src/services/user_service.rb"
operation:
  type: "edit"
  description: "Add null check for user parameter"
  changes:
    - line: 42
      old: "user.email"
      new: "user&.email"
checkpoint_id: "chk-20240115-001"
```

**Output:**
```yaml
success: true
target: "src/services/user_service.rb"
operation: "Added safe navigation operator for null user handling"
previous_state:
  snapshot: "def get_email(user)\n  user.email\nend"
  captured_at: "2024-01-15T10:30:00Z"
new_state:
  snapshot: "def get_email(user)\n  user&.email\nend"
  verified_at: "2024-01-15T10:30:01Z"
diff:
  type: "unified"
  content: |
    @@ -42 +42 @@
    -  user.email
    +  user&.email
checkpoint_id: "chk-20240115-001"
rollback_command: "git checkout src/services/user_service.rb"
evidence_anchors:
  - "src/services/user_service.rb:42"
```

### Example 2: Database Mutation

**Input:**
```yaml
target: "users table"
operation:
  type: "sql"
  description: "Add status column with default value"
  sql: "ALTER TABLE users ADD COLUMN status VARCHAR(20) DEFAULT 'active'"
checkpoint_id: "chk-20240115-002"
```

**Output:**
```yaml
success: true
target: "users table"
operation: "Added status column with default 'active'"
previous_state:
  snapshot:
    columns: ["id", "email", "created_at"]
  captured_at: "2024-01-15T11:00:00Z"
new_state:
  snapshot:
    columns: ["id", "email", "created_at", "status"]
  verified_at: "2024-01-15T11:00:05Z"
diff:
  type: "structural"
  content: "+ status VARCHAR(20) DEFAULT 'active'"
checkpoint_id: "chk-20240115-002"
rollback_command: "ALTER TABLE users DROP COLUMN status"
evidence_anchors:
  - "command:psql:schema_after"
```

### Example 3: Mutation Failure

**Input:**
```yaml
target: "config/database.yml"
operation:
  type: "edit"
  description: "Update connection pool size"
checkpoint_id: "chk-20240115-003"
```

**Output:**
```yaml
success: false
target: "config/database.yml"
operation: "Update connection pool size (FAILED)"
previous_state:
  snapshot: "pool: 5"
  captured_at: "2024-01-15T12:00:00Z"
new_state:
  snapshot: null
  verified_at: null
diff:
  type: "none"
  content: "Mutation failed: file locked by another process"
checkpoint_id: "chk-20240115-003"
rollback_command: "N/A - mutation did not complete"
evidence_anchors:
  - "error:file_locked"
error:
  message: "File locked by another process"
  recoverable: true
  suggestion: "Retry after process releases lock"
```

## Verification

- [ ] Checkpoint exists and is valid
- [ ] Previous state captured before mutation
- [ ] New state verified after mutation
- [ ] Diff accurately reflects change
- [ ] Rollback command is correct

**Verification tools:** Read (to verify state changes)

## Safety Constraints

- `mutation`: true
- `requires_checkpoint`: true
- `requires_approval`: true
- `risk`: high

**Capability-specific rules:**
- NEVER mutate without valid checkpoint
- Always capture previous state before modification
- Verify change matches intended operation
- Provide working rollback mechanism
- Stop immediately on unexpected errors
- Do not chain multiple mutations without intermediate checkpoints

## Composition Patterns

**Commonly follows:**
- `checkpoint` - REQUIRED before any mutation
- `plan` - Mutations execute planned changes
- `verify` - Verify preconditions before mutating

**Commonly precedes:**
- `verify` - Verify mutation results
- `audit` - Record mutation for audit trail
- `rollback` - Undo mutation if verification fails

**Anti-patterns:**
- NEVER mutate without checkpoint
- Never combine multiple risky mutations
- Avoid mutation in exploratory workflows

**Workflow references:**
- See `reference/workflow_catalog.yaml#debug_code_change` for mutation in bug fixes
- See `reference/workflow_catalog.yaml#digital_twin_sync_loop` for mutation in sync loops
