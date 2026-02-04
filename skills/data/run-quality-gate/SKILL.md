---
name: run-quality-gate
description: Execute quality gate validation with configurable blocking behavior. Use when running type-check, build, tests, lint, or custom validation commands in orchestrators or workers to enforce quality standards.
allowed-tools: Bash, Read
---

# Run Quality Gate

Execute validation commands as quality gates with configurable blocking/non-blocking behavior and structured error reporting.

## When to Use

- Type-check validation in pre-flight or quality gates
- Build validation before releases
- Test execution as quality gate
- Lint validation for code quality
- Custom validation commands
- Orchestrator phase validation
- Worker self-validation

## Instructions

### Step 1: Receive Gate Configuration

Accept gate configuration as input.

**Expected Input**:

```json
{
  "gate": "type-check|build|tests|lint|custom",
  "blocking": true,
  "custom_command": "pnpm custom-validate"
}
```

**Parameters**:

- `gate`: Type of quality gate to run (required)
- `blocking`: Whether failure should stop workflow (default: true)
- `custom_command`: Command to run when gate="custom" (required for custom gates)

### Step 2: Map Gate to Command

Determine command to execute based on gate type.

**Gate Commands**:

- `type-check` → `pnpm type-check`
- `build` → `pnpm build`
- `tests` → `pnpm test`
- `lint` → `pnpm lint`
- `custom` → Use `custom_command` parameter

**Validation**:

- If gate="custom", `custom_command` must be provided
- Command must be valid shell command

### Step 3: Execute Command

Run command via Bash tool with timeout.

**Execution Parameters**:

- Timeout: 300000ms (5 minutes)
- Capture stdout and stderr
- Record exit code
- Track execution duration

**Tools Used**: Bash

### Step 4: Parse Exit Code and Output

Determine if gate passed based on exit code.

**Pass/Fail Logic**:

- Exit code 0 → Passed
- Exit code non-zero → Failed

**Extract Errors**:
Look for error patterns in output:

- Lines containing "error"
- Lines containing "failed"
- Lines containing "✗"
- TypeScript error codes (TS####)
- Stack traces

### Step 5: Determine Action

Calculate action based on result and blocking flag.

**Action Logic**:

```
IF exit_code == 0:
  action = "continue"
  passed = true
ELSE:
  IF blocking == true:
    action = "stop"
  ELSE:
    action = "warn"
  passed = false
```

### Step 6: Return Structured Result

Return complete quality gate result.

**Expected Output**:

```json
{
  "gate": "type-check",
  "passed": true,
  "blocking": true,
  "action": "continue",
  "errors": [],
  "exit_code": 0,
  "duration_ms": 2345,
  "command": "pnpm type-check",
  "timestamp": "2025-10-18T14:30:00Z"
}
```

**Output Fields**:

- `gate`: Gate type that was run
- `passed`: Whether gate passed (boolean)
- `blocking`: Whether gate was blocking
- `action`: Action to take (continue|stop|warn)
- `errors`: Array of error messages extracted
- `exit_code`: Command exit code
- `duration_ms`: Execution time in milliseconds
- `command`: Actual command executed
- `timestamp`: ISO-8601 timestamp of execution

## Error Handling

- **Timeout (5 minutes)**: Return failed with timeout error
- **Missing custom_command**: Return error requesting custom_command
- **Invalid gate type**: Return error listing valid gates
- **Command not found**: Return failed with command not found error
- **Empty output but non-zero exit**: Return failed with generic error

## Examples

### Example 1: Blocking Type-Check that Passes

**Input**:

```json
{
  "gate": "type-check",
  "blocking": true
}
```

**Command Output**:

```
$ pnpm type-check
✓ No type errors found
Done in 2.3s
```

**Output**:

```json
{
  "gate": "type-check",
  "passed": true,
  "blocking": true,
  "action": "continue",
  "errors": [],
  "exit_code": 0,
  "duration_ms": 2345,
  "command": "pnpm type-check",
  "timestamp": "2025-10-18T14:30:00Z"
}
```

### Example 2: Blocking Build that Fails (Should Stop)

**Input**:

```json
{
  "gate": "build",
  "blocking": true
}
```

**Command Output**:

```
$ pnpm build
✗ Build failed
ERROR in src/app.ts
Module not found: Error: Can't resolve 'missing-module'
exit code: 1
```

**Output**:

```json
{
  "gate": "build",
  "passed": false,
  "blocking": true,
  "action": "stop",
  "errors": ["ERROR in src/app.ts", "Module not found: Error: Can't resolve 'missing-module'"],
  "exit_code": 1,
  "duration_ms": 5432,
  "command": "pnpm build",
  "timestamp": "2025-10-18T14:30:05Z"
}
```

### Example 3: Non-Blocking Lint that Fails (Should Warn)

**Input**:

```json
{
  "gate": "lint",
  "blocking": false
}
```

**Command Output**:

```
$ pnpm lint
✗ 12 problems (8 errors, 4 warnings)
src/utils.ts:10:5 - error - Missing semicolon
src/app.ts:25:1 - warning - Prefer const over let
exit code: 1
```

**Output**:

```json
{
  "gate": "lint",
  "passed": false,
  "blocking": false,
  "action": "warn",
  "errors": [
    "src/utils.ts:10:5 - error - Missing semicolon",
    "src/app.ts:25:1 - warning - Prefer const over let"
  ],
  "exit_code": 1,
  "duration_ms": 1234,
  "command": "pnpm lint",
  "timestamp": "2025-10-18T14:30:07Z"
}
```

### Example 4: Custom Command Example

**Input**:

```json
{
  "gate": "custom",
  "blocking": true,
  "custom_command": "pnpm validate-schemas"
}
```

**Command Output**:

```
$ pnpm validate-schemas
✓ All schemas valid
exit code: 0
```

**Output**:

```json
{
  "gate": "custom",
  "passed": true,
  "blocking": true,
  "action": "continue",
  "errors": [],
  "exit_code": 0,
  "duration_ms": 876,
  "command": "pnpm validate-schemas",
  "timestamp": "2025-10-18T14:30:08Z"
}
```

### Example 5: Timeout Example

**Input**:

```json
{
  "gate": "tests",
  "blocking": true
}
```

**Output** (after 5 minutes):

```json
{
  "gate": "tests",
  "passed": false,
  "blocking": true,
  "action": "stop",
  "errors": ["Command timed out after 300000ms (5 minutes)"],
  "exit_code": -1,
  "duration_ms": 300000,
  "command": "pnpm test",
  "timestamp": "2025-10-18T14:35:00Z"
}
```

### Example 6: Command Not Found

**Input**:

```json
{
  "gate": "build",
  "blocking": true
}
```

**Command Output**:

```
bash: pnpm: command not found
exit code: 127
```

**Output**:

```json
{
  "gate": "build",
  "passed": false,
  "blocking": true,
  "action": "stop",
  "errors": ["bash: pnpm: command not found"],
  "exit_code": 127,
  "duration_ms": 45,
  "command": "pnpm build",
  "timestamp": "2025-10-18T14:30:09Z"
}
```

## Validation

- [ ] Maps all standard gate types to correct commands
- [ ] Executes commands with 5 minute timeout
- [ ] Captures exit code correctly
- [ ] Extracts errors from output
- [ ] Determines action correctly based on blocking flag
- [ ] Records execution duration
- [ ] Handles timeout gracefully
- [ ] Validates custom_command when gate="custom"
- [ ] Returns structured JSON output

## Integration with Agents

### Orchestrator Usage

```markdown
## Quality Gate: Type Check

Use run-quality-gate Skill with gate="type-check" and blocking=true.

If action="stop", halt workflow and report failure.
If action="continue", proceed to next phase.
```

### Worker Self-Validation

```markdown
## Step 5: Self-Validation

Use run-quality-gate Skill to validate changes:

1. Run type-check (blocking=true)
2. Run build (blocking=true)
3. Run tests (blocking=false)

If any blocking gate returns action="stop", rollback changes.
```

### Quality Gates Orchestrator

```markdown
## Phase 2: Execute Quality Gates

For each gate in [type-check, build, tests, lint]:
result = run-quality-gate(gate, blocking=true)

if result.action == "stop":
HALT and report failure

if result.action == "warn":
LOG warning and continue
```

## Supporting Files

- `gate-mappings.json`: Gate command mappings and configurations (see below)

## Notes

- Timeout is fixed at 5 minutes to prevent indefinite hangs
- Error extraction is best-effort (may not capture all errors)
- Custom commands must be valid shell commands
- Exit code 0 always means success regardless of output
- Non-zero exit code always means failure
- Blocking flag only affects action, not passed status
