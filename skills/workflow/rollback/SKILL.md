---
name: rollback
description: Safely undo changes by restoring to a checkpoint. Use when verify fails, errors occur, or explicit undo is requested. Essential for the CAVR pattern recovery.
argument-hint: "[checkpoint_id] [scope] [verify_restore]"
disable-model-invocation: false
user-invocable: true
allowed-tools: Read, Bash, Git
context: fork
agent: general-purpose
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: prompt
          prompt: |
            ROLLBACK SAFETY VALIDATION

            Rollback command: {{tool_input.command}}

            Before executing rollback, verify:
            1. Target checkpoint ID exists and is valid
            2. Checkpoint has not expired
            3. Current state has been captured (for audit)
            4. Rollback scope matches intended restore scope
            5. No ongoing operations that would conflict

            CRITICAL CHECKS:
            - Is checkpoint integrity verified (hash match)?
            - Will any data be irreversibly lost?
            - Are there uncommitted changes that would be overwritten?

            Reply ALLOW if rollback is safe to execute.
            Reply BLOCK with reason if:
            - Checkpoint is missing or corrupted
            - Rollback would cause data loss beyond intended scope
            - Current state needs to be preserved first
          once: false
        - type: command
          command: |
            # Verify checkpoint exists before rollback
            CMD="{{tool_input.command}}"
            if echo "$CMD" | grep -q "git stash"; then
              # Check if there are stashes to pop
              if ! git stash list 2>/dev/null | head -1 | grep -q .; then
                echo "BLOCK: No git stash found to restore"
                exit 1
              fi
            fi
            exit 0
  PostToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: |
            echo "[ROLLBACK] $(date -u +%Y-%m-%dT%H:%M:%SZ) | Command: {{tool_input.command}} | Exit: {{tool_output.exit_code}}" >> .audit/rollback-operations.log 2>/dev/null || true
---

## Intent

Execute **rollback** to restore system state to a previously created checkpoint. This is the recovery mechanism in the CAVR (Checkpoint-Act-Verify-Rollback) pattern - used when mutations fail or produce undesired outcomes.

**Success criteria:**
- State fully restored to checkpoint state
- Post-rollback hash matches checkpoint hash
- No orphaned artifacts remain from failed mutation
- Audit trail of what was reverted

**Compatible schemas:**
- `schemas/output_schema.yaml`

## Inputs

| Parameter | Required | Type | Description |
|-----------|----------|------|-------------|
| `checkpoint_id` | Yes | string | ID of checkpoint to restore to |
| `scope` | No | array | Specific files/keys to rollback (default: all in checkpoint) |
| `verify_restore` | No | boolean | Whether to verify state matches checkpoint after restore (default: true) |
| `reason` | No | string | Why rollback is being performed (for audit) |

## Procedure

1) **Validate checkpoint**: Confirm checkpoint exists and is valid
   - Look up checkpoint by ID in `.checkpoints/` or git stash
   - Verify checkpoint integrity (hash check)
   - Confirm checkpoint has not expired
   - If checkpoint missing: FAIL immediately with clear error

2) **Capture current state**: Record what will be reverted
   - List all files/state that differ from checkpoint
   - Compute hash of current state for audit
   - Document changes that will be undone

3) **Execute restoration**: Apply the restore command
   - For git_stash: `git stash pop` or `git stash apply`
   - For file_backup: Copy from `.checkpoints/<id>/` to original locations
   - For state_snapshot: Restore state variables
   - Handle any conflicts or errors gracefully

4) **Verify restoration**: Confirm state matches checkpoint
   - Recompute hash of restored state
   - Compare with checkpoint's pre_mutation_state.hash
   - Check for orphaned files created during failed mutation
   - Clean up orphaned artifacts if present

5) **Ground claims**: Attach evidence of successful rollback
   - Format: `tool:bash:<restore_command>`, comparison output
   - Include before/after state hashes

6) **Format output**: Return rollback results per contract

## Output Contract

Return a structured object:

```yaml
rolled_back: boolean
restored_to:
  checkpoint_id: string
  checkpoint_type: string
  timestamp: string  # When checkpoint was created
changes_reverted:
  - file: string
    operation: string  # What was undone (create, modify, delete)
    summary: string  # Brief description of change reverted
verification:
  pre_state_hash: string  # Hash before rollback
  post_state_hash: string  # Hash after rollback
  checkpoint_hash: string  # Expected hash from checkpoint
  match: boolean  # post_state_hash == checkpoint_hash
warnings: array[string]  # Any issues encountered
next_actions: array[string]  # Suggested follow-up
confidence: number  # 0.0-1.0
evidence_anchors: ["tool:bash:...", "file:..."]
assumptions: []
```

### Field Definitions

| Field | Type | Description |
|-------|------|-------------|
| `rolled_back` | boolean | Whether rollback was successful |
| `restored_to` | object | Checkpoint that was restored to |
| `changes_reverted` | array | List of changes that were undone |
| `verification.match` | boolean | Whether restored state matches checkpoint |
| `warnings` | array | Issues like orphaned files or partial restore |
| `next_actions` | array | What to do next (re-plan, investigate, etc.) |
| `confidence` | number | 0.0-1.0 based on verification match |
| `evidence_anchors` | array | Proof of restoration |
| `assumptions` | array | Explicit assumptions made |

## Examples

### Example 1: Git Stash Rollback After Failed Tests

**Input:**
```yaml
checkpoint_id: "chk_20240115_143022_a7b3c9"
verify_restore: true
reason: "Tests failed after refactoring"
```

**Output:**
```yaml
rolled_back: true
restored_to:
  checkpoint_id: "chk_20240115_143022_a7b3c9"
  checkpoint_type: git_stash
  timestamp: "2024-01-15T14:30:22Z"
changes_reverted:
  - file: "src/api/handlers/user.py"
    operation: modify
    summary: "Reverted refactored get_user() function"
  - file: "src/api/handlers/auth.py"
    operation: modify
    summary: "Reverted auth token validation changes"
verification:
  pre_state_hash: "sha256:deadbeef..."
  post_state_hash: "sha256:e3b0c442..."
  checkpoint_hash: "sha256:e3b0c442..."
  match: true
warnings: []
next_actions:
  - "critique: Analyze why refactoring broke tests"
  - "plan: Create new plan with smaller incremental changes"
confidence: 1.0
evidence_anchors:
  - "tool:bash:git stash pop stash@{0}"
  - "tool:bash:git diff --stat HEAD"
  - "tool:bash:sha256sum src/api/handlers/*.py"
assumptions:
  - "No other changes made to stashed files since checkpoint"
```

**Evidence pattern:** Git stash pop output, diff showing restored state, hash verification.

---

### Example 2: File Backup Rollback with Orphaned Files

**Input:**
```yaml
checkpoint_id: "chk_20240115_150000_config"
verify_restore: true
reason: "Config migration caused service failure"
```

**Output:**
```yaml
rolled_back: true
restored_to:
  checkpoint_id: "chk_20240115_150000_config"
  checkpoint_type: file_backup
  timestamp: "2024-01-15T15:00:00Z"
changes_reverted:
  - file: "config/production.yaml"
    operation: modify
    summary: "Reverted database connection string changes"
verification:
  pre_state_hash: "sha256:newconfig..."
  post_state_hash: "sha256:abc123..."
  checkpoint_hash: "sha256:abc123..."
  match: true
warnings:
  - "Orphaned file detected: config/production.yaml.bak (removed)"
next_actions:
  - "audit: Record failed migration attempt"
  - "plan: Investigate migration script issue"
confidence: 0.95
evidence_anchors:
  - "tool:bash:cp .checkpoints/chk_20240115_150000_config/production.yaml config/"
  - "tool:bash:rm config/production.yaml.bak"
  - "file:config/production.yaml:1"
assumptions:
  - "Checkpoint backup file is not corrupted"
```

## Verification

Apply the following verification patterns:

- [ ] **Rollback Verification**: post_state_hash == checkpoint_hash (CRITICAL)
- [ ] **State Assertion**: No unexpected files remain after rollback
- [ ] **Evidence Grounding**: Restore command execution is captured
- [ ] **Clean Git State**: git status shows no unexpected changes

**Verification tools:** Bash (for restore and hash), Git (for stash operations)

## Safety Constraints

- `mutation`: true (modifies files to restore state)
- `requires_checkpoint`: true (MUST have valid checkpoint to rollback to)
- `requires_approval`: false
- `risk`: medium

**Capability-specific rules:**
- CRITICAL: Never rollback without valid checkpoint_id
- CRITICAL: Always verify state hash matches after restore
- Clean up orphaned files created by failed mutation
- Do not rollback if checkpoint has expired
- Preserve audit trail of what was reverted
- If verification fails, STOP and alert - do not proceed

## Composition Patterns

**Commonly follows:**
- `verify` - When verify returns FAIL, trigger rollback (CAVR pattern)
- `act-plan` - If act-plan encounters error, rollback
- `checkpoint` - Rollback requires prior checkpoint (dependency)

**Commonly precedes:**
- `critique` - After rollback, analyze what went wrong
- `plan` - Create new plan after understanding failure
- `audit` - Record the rollback event

**Anti-patterns:**
- CRITICAL: Never rollback without existing checkpoint
- CRITICAL: Never continue mutations after rollback without new checkpoint
- Never skip verification after rollback
- Never delete checkpoint until rollback verification passes

**Workflow references:**
- See `reference/composition_patterns.md#checkpoint-act-verify-rollback` for CAVR pattern
- See `reference/composition_patterns.md#rollback-verification` in verification_patterns.md
- See `reference/composition_patterns.md#debug-code-change` for rollback-then-critique flow
