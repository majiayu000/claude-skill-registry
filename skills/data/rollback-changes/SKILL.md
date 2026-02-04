---
name: rollback-changes
description: Automatically rollback changes from failed workflow phases using changes log files. Use when workflows fail and need to restore previous state, including file restoration, artifact cleanup, and command reversal. Use for error recovery after failed bug fixes, security patches, or refactoring operations.
allowed-tools: Bash, Read, Write
---

# Rollback Changes

Automatically rollback changes from failed workflow phases by reading changes log files and reversing all tracked modifications.

## When to Use

- Workflow phase fails and needs state restoration
- Automated rollback after failed bug fixes
- Restore previous state after failed security patches
- Cleanup after failed refactoring operations
- Error recovery in worker agents
- Quality gate failures requiring revert

## Instructions

### Step 1: Read Changes Log File

Use Read tool to load the changes log file.

**Expected Input**:

- `changes_log_path`: String (path to changes log JSON, e.g., `.bug-changes.json`)
- `phase`: String (workflow phase name, e.g., "bug-fixing")
- `confirmation_required`: Boolean (default: true, ask user before rollback)

**Tools Used**: Read

### Step 2: Parse Changes Log

Parse the JSON content and validate structure.

**Required Fields**:

- `phase`: String (workflow phase that made changes)
- `timestamp`: String (ISO-8601 timestamp)
- `files_modified`: Array of objects with `{path, backup}` (files with backups)
- `files_created`: Array of strings (new files created)
- `commands_executed`: Array of strings (commands that were run)
- `git_commits`: Array of strings (commit SHAs if any)

**Optional Fields**:

- `artifacts`: Array of strings (temporary files to remove)
- `plan_files`: Array of strings (plan files to remove)
- `metadata`: Object (additional context)

### Step 3: Request Confirmation (if required)

If `confirmation_required` is true, ask user for confirmation.

**Confirmation Prompt**:

```
Rollback changes from phase "{phase}"?

Changes to revert:
- Files modified: {count}
- Files created: {count}
- Commands executed: {count}
- Git commits: {count}

This action will:
1. Restore {count} files from backups
2. Delete {count} created files
3. Revert {count} commands
4. Revert {count} git commits

Proceed with rollback? (yes/no)
```

**If user says "no"**: Return without taking action (dry run result)

**If `confirmation_required` is false**: Skip confirmation and proceed

### Step 4: Restore Modified Files

For each file in `files_modified`, restore from backup.

**Restoration Process**:

```bash
# For each {path, backup} in files_modified:
if [ -f "{backup}" ]; then
  cp "{backup}" "{path}"
  echo "✓ Restored {path} from {backup}"
else
  echo "⚠ Backup not found: {backup} (skipping)"
fi
```

**Error Handling**:

- Missing backup file: Log warning, continue with other files
- Copy failure: Log error, continue with other files
- Permission issues: Log error, continue with other files

**Tools Used**: Bash

### Step 5: Delete Created Files

For each file in `files_created`, delete if it exists.

**Deletion Process**:

```bash
# For each file in files_created:
if [ -f "{file}" ]; then
  rm "{file}"
  echo "✓ Deleted created file: {file}"
elif [ -d "{file}" ]; then
  rm -rf "{file}"
  echo "✓ Deleted created directory: {file}"
else
  echo "⚠ File not found (already deleted?): {file}"
fi
```

**Error Handling**:

- File not found: Log warning (may already be deleted)
- Permission issues: Log error, continue with other files
- Directory not empty: Use `rm -rf` with caution

**Tools Used**: Bash

### Step 6: Revert Commands

For each command in `commands_executed`, attempt to revert.

**Revert Mapping**:

- `pnpm install` → `pnpm install` (re-run to restore lockfile)
- `git add {files}` → `git restore --staged {files}`
- `git commit` → Handled in Step 7
- `pnpm build` → `rm -rf dist/` (remove build artifacts)
- Custom commands → Log only (cannot automatically revert)

**Revert Process**:

```bash
# For each command:
case "{command}" in
  "pnpm install")
    pnpm install
    echo "✓ Re-ran pnpm install to restore dependencies"
    ;;
  "git add "*)
    git restore --staged .
    echo "✓ Unstaged all files"
    ;;
  "pnpm build")
    rm -rf dist/
    echo "✓ Removed build artifacts"
    ;;
  *)
    echo "⚠ Cannot auto-revert: {command} (manual intervention required)"
    ;;
esac
```

**Error Handling**:

- Command fails: Log error, continue with other commands
- Unknown command: Log warning, cannot revert
- Already reverted: Log info, continue

**Tools Used**: Bash

### Step 7: Revert Git Commits

For each commit SHA in `git_commits`, revert the commit.

**Revert Process**:

```bash
# For each SHA in git_commits (in reverse order):
git revert --no-edit {sha}
if [ $? -eq 0 ]; then
  echo "✓ Reverted commit {sha}"
else
  echo "❌ Failed to revert commit {sha} (may have conflicts)"
fi
```

**Error Handling**:

- Revert conflicts: Log error, provide manual instructions
- Commit not found: Log error, skip commit
- Detached HEAD: Log error, skip git operations

**Tools Used**: Bash

### Step 8: Cleanup Artifacts

Remove temporary files and plan files.

**Cleanup Process**:

```bash
# Remove plan files
rm -f .{workflow}-plan.json

# Remove other artifacts if specified
for artifact in {artifacts}; do
  rm -f "{artifact}"
  echo "✓ Removed artifact: {artifact}"
done

# Remove rollback backups (optional, only if all succeeded)
if [ {all_succeeded} == true ]; then
  rm -rf .rollback/
  echo "✓ Removed rollback backups"
fi
```

**Tools Used**: Bash

### Step 9: Generate Rollback Report

Create a structured report of all actions taken.

**Report Structure**:

```json
{
  "success": true|false,
  "phase": "bug-fixing",
  "actions_taken": [
    "Restored 3 files from backups",
    "Deleted 2 created files",
    "Reverted 1 git commit",
    "Cleaned up 2 artifacts"
  ],
  "files_restored": 3,
  "files_deleted": 2,
  "commands_reverted": 1,
  "git_commits_reverted": 1,
  "artifacts_cleaned": 2,
  "errors": [],
  "warnings": [
    "Backup not found: .rollback/file.backup (skipped)"
  ],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 1234
}
```

**Tools Used**: Write

### Step 10: Return Structured Output

Return complete rollback result.

**Expected Output**:

```json
{
  "success": true,
  "phase": "bug-fixing",
  "actions_taken": [
    "Restored src/app.ts from .rollback/src-app.ts.backup",
    "Deleted src/new-file.ts",
    "Reverted git commit abc123",
    "Removed artifact .bug-fixing-plan.json"
  ],
  "files_restored": 1,
  "files_deleted": 1,
  "commands_reverted": 0,
  "git_commits_reverted": 1,
  "artifacts_cleaned": 1,
  "errors": [],
  "warnings": [],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 1234
}
```

## Error Handling

- **Missing Changes Log**: Return error "Changes log not found at {path}"
- **Invalid JSON**: Return error "Invalid JSON in changes log: {details}"
- **Missing Required Fields**: Return error "Changes log missing required field: {field}"
- **Backup Not Found**: Log warning, continue with other files (partial rollback)
- **File Deletion Failed**: Log error, continue with other files
- **Git Revert Failed**: Log error with conflict details, continue with other operations
- **User Declined**: Return dry run result with `success: false, user_declined: true`
- **Partial Rollback**: Return `success: true` with warnings array documenting issues

## Examples

### Example 1: Full Rollback (All Operations Succeed)

**Input**:

```json
{
  "changes_log_path": ".bug-changes.json",
  "phase": "bug-fixing",
  "confirmation_required": false
}
```

**Changes Log Content**:

```json
{
  "phase": "bug-fixing",
  "timestamp": "2025-10-18T14:30:00Z",
  "files_modified": [
    { "path": "src/app.ts", "backup": ".rollback/src-app.ts.backup" },
    { "path": "src/utils.ts", "backup": ".rollback/src-utils.ts.backup" }
  ],
  "files_created": ["src/new-helper.ts"],
  "commands_executed": ["pnpm install", "pnpm build"],
  "git_commits": ["abc123def456"],
  "artifacts": [".bug-fixing-plan.json"]
}
```

**Output**:

```json
{
  "success": true,
  "phase": "bug-fixing",
  "actions_taken": [
    "Restored src/app.ts from .rollback/src-app.ts.backup",
    "Restored src/utils.ts from .rollback/src-utils.ts.backup",
    "Deleted src/new-helper.ts",
    "Re-ran pnpm install to restore dependencies",
    "Removed build artifacts (dist/)",
    "Reverted git commit abc123def456",
    "Removed artifact .bug-fixing-plan.json"
  ],
  "files_restored": 2,
  "files_deleted": 1,
  "commands_reverted": 2,
  "git_commits_reverted": 1,
  "artifacts_cleaned": 1,
  "errors": [],
  "warnings": [],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 2345
}
```

### Example 2: Partial Rollback (Some Backups Missing)

**Input**:

```json
{
  "changes_log_path": ".security-changes.json",
  "phase": "security-remediation",
  "confirmation_required": false
}
```

**Changes Log Content**:

```json
{
  "phase": "security-remediation",
  "timestamp": "2025-10-18T14:30:00Z",
  "files_modified": [
    { "path": "src/auth.ts", "backup": ".rollback/src-auth.ts.backup" },
    { "path": "src/db.ts", "backup": ".rollback/src-db.ts.backup" }
  ],
  "files_created": ["src/new-auth.ts"],
  "commands_executed": [],
  "git_commits": []
}
```

**Scenario**: Backup for `src/db.ts` is missing

**Output**:

```json
{
  "success": true,
  "phase": "security-remediation",
  "actions_taken": [
    "Restored src/auth.ts from .rollback/src-auth.ts.backup",
    "Deleted src/new-auth.ts"
  ],
  "files_restored": 1,
  "files_deleted": 1,
  "commands_reverted": 0,
  "git_commits_reverted": 0,
  "artifacts_cleaned": 0,
  "errors": [],
  "warnings": ["Backup not found: .rollback/src-db.ts.backup (file not restored)"],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 456
}
```

### Example 3: Dry Run (User Declines)

**Input**:

```json
{
  "changes_log_path": ".refactor-changes.json",
  "phase": "refactoring",
  "confirmation_required": true
}
```

**User Response**: "no"

**Output**:

```json
{
  "success": false,
  "phase": "refactoring",
  "user_declined": true,
  "actions_taken": [],
  "files_restored": 0,
  "files_deleted": 0,
  "commands_reverted": 0,
  "git_commits_reverted": 0,
  "artifacts_cleaned": 0,
  "errors": [],
  "warnings": [],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 0
}
```

### Example 4: No Changes Log (File Missing)

**Input**:

```json
{
  "changes_log_path": ".nonexistent-changes.json",
  "phase": "unknown",
  "confirmation_required": false
}
```

**Output**:

```json
{
  "success": false,
  "phase": "unknown",
  "actions_taken": [],
  "files_restored": 0,
  "files_deleted": 0,
  "commands_reverted": 0,
  "git_commits_reverted": 0,
  "artifacts_cleaned": 0,
  "errors": ["Changes log not found at .nonexistent-changes.json"],
  "warnings": [],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 10
}
```

### Example 5: Git Revert with Conflicts

**Input**:

```json
{
  "changes_log_path": ".bug-changes.json",
  "phase": "bug-fixing",
  "confirmation_required": false
}
```

**Changes Log Content**:

```json
{
  "phase": "bug-fixing",
  "timestamp": "2025-10-18T14:30:00Z",
  "files_modified": [],
  "files_created": [],
  "commands_executed": [],
  "git_commits": ["abc123", "def456"]
}
```

**Scenario**: Reverting `abc123` causes conflicts

**Output**:

```json
{
  "success": true,
  "phase": "bug-fixing",
  "actions_taken": ["Reverted git commit def456"],
  "files_restored": 0,
  "files_deleted": 0,
  "commands_reverted": 0,
  "git_commits_reverted": 1,
  "artifacts_cleaned": 0,
  "errors": ["Failed to revert commit abc123: Merge conflict in src/app.ts"],
  "warnings": ["Manual resolution required for commit abc123"],
  "timestamp": "2025-10-18T14:45:00Z",
  "duration_ms": 876
}
```

## Validation

- [ ] Reads and parses changes log correctly
- [ ] Requests user confirmation when required
- [ ] Restores files from backups successfully
- [ ] Deletes created files correctly
- [ ] Reverts commands appropriately
- [ ] Handles git revert operations
- [ ] Cleans up artifacts
- [ ] Generates structured report
- [ ] Handles partial rollback gracefully
- [ ] Returns clear error messages for failures
- [ ] Logs warnings for non-critical issues
- [ ] Completes within reasonable time (< 30 seconds typical)

## Safety Features

### Confirmation by Default

- Always ask for confirmation unless explicitly disabled
- Show clear summary of what will be reverted
- Allow user to cancel before any changes

### Partial Rollback Acceptable

- Don't fail entirely if some backups are missing
- Continue with other operations when one fails
- Document all issues in warnings array

### No Silent Failures

- Log all errors and warnings explicitly
- Return detailed actions_taken array
- Provide troubleshooting context in errors

### Backup Verification

- Never delete original files without verifying backup exists
- Check backup file exists before restoration
- Preserve backups until full rollback succeeds

### Audit Trail

- Log all rollback actions for debugging
- Include timestamps and durations
- Return complete report for documentation

## Integration with Workers

Workers should create changes log files during operations:

```markdown
## Step 2: Track Changes

Before making any modifications:

1. Create changes log: `.{domain}-changes.json`
2. For each file modified:
   - Create backup in `.rollback/{path}.backup`
   - Add to `files_modified` array
3. For each file created:
   - Add to `files_created` array
4. For each command executed:
   - Add to `commands_executed` array
5. For each git commit:
   - Add SHA to `git_commits` array
6. Write changes log after each modification

## Step 5: Rollback on Failure

If quality gate fails or error occurs:

1. Use rollback-changes Skill with:
   - changes_log_path: ".{domain}-changes.json"
   - phase: "{current-phase}"
   - confirmation_required: false (automated rollback)
2. If rollback succeeds, report clean state
3. If rollback fails, report partial state with warnings
```

## Supporting Files

- `changes-log-schema.json`: JSON schema for changes log format (see below)

## Notes

- Rollback operations are best-effort (may not be 100% reversible)
- Git revert operations may require manual conflict resolution
- Some commands (custom scripts) cannot be automatically reverted
- Backups should be stored in `.rollback/` directory (gitignored)
- Changes log files should be temporary (removed after successful completion)
- Partial rollback is acceptable and documented in warnings
- Always verify backup exists before deletion operations
