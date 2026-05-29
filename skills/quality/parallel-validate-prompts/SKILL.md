---
name: parallel-validate-prompts
description: Validate and fix parallel prompts for required sections
argument-hint: <parallel-dir> [--fix] [--verbose]
---

# parallel-validate-prompts

**Category**: Parallel Development

## Usage

```bash
/parallel-validate-prompts <parallel-dir> [--fix] [--verbose]
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `<parallel-dir>` | Yes | Path to parallel folder (e.g., `parallel/TS-0042-inventory/`) |
| `--fix` | No | Automatically regenerate non-compliant prompts |
| `--verbose` | No | Show detailed validation for each prompt |

## Purpose

Validate that generated prompt files in `prompts/` contain all required sections for successful agent execution. This command:

1. Scans all `prompts/task-*.txt` files
2. Validates presence of mandatory sections
3. Reports compliance status
4. Optionally regenerates non-compliant prompts

Use this to verify prompts generated elsewhere (other tools, manual creation, or older decomposition runs) before running `cpo run`.

## Required Sections

Every prompt file MUST contain these sections (see `parallel-prompt-generator` skill):

| Section | Marker | Purpose |
|---------|--------|---------|
| **Skills** | `=== REQUIRED SKILLS ===` | Skills to invoke at start |
| Context | `=== CONTEXT ===` | Shared project context |
| Objective | `=== OBJECTIVE ===` | Task goal |
| Contracts | `=== CONTRACTS ===` | Contract file references |
| Files to Create | `=== FILES TO CREATE ===` | Scope CREATE |
| Files to Modify | `=== FILES TO MODIFY ===` | Scope MODIFY |
| Do Not Modify | `=== DO NOT MODIFY ===` | Scope BOUNDARY |
| Requirements | `=== IMPLEMENTATION REQUIREMENTS ===` | Implementation details |
| Acceptance | `=== ACCEPTANCE CRITERIA ===` | Checklist items |
| **Execution** | `=== EXECUTION INSTRUCTIONS ===` | How to implement |
| **Rules** | `=== IMPORTANT RULES ===` | Constraints |
| **Output Format** | `=== OUTPUT FORMAT (REQUIRED) ===` | JSON output block |
| **Completion** | `=== COMPLETION SIGNAL ===` | touch .claude-task-complete |

The last four sections (bold) are **critical** - prompts missing these will fail to produce structured output.

---

## Execution Instructions for Claude Code

When this command is run, Claude Code should:

### 1. Parse Arguments

```
PARALLEL_DIR = first positional argument
FIX_MODE = true if --fix specified
VERBOSE = true if --verbose specified
```

### 2. Validate Directory Structure

Check that the parallel directory exists and has prompts:

```bash
ls "$PARALLEL_DIR/prompts/task-*.txt" 2>/dev/null
```

If no prompts found:
```
ERROR: No prompt files found in $PARALLEL_DIR/prompts/

Expected files: prompts/task-001.txt, prompts/task-002.txt, etc.

Run '/parallel-decompose' to generate prompts, or create them manually.
```

### 3. Validate Each Prompt File

For each `prompts/task-*.txt` file, check for required markers:

```python
REQUIRED_SECTIONS = [
    ("REQUIRED SKILLS", "=== REQUIRED SKILLS ==="),
    ("CONTEXT", "=== CONTEXT ==="),
    ("OBJECTIVE", "=== OBJECTIVE ==="),
    ("CONTRACTS", "=== CONTRACTS ==="),
    ("FILES TO CREATE", "=== FILES TO CREATE ==="),
    ("FILES TO MODIFY", "=== FILES TO MODIFY ==="),
    ("DO NOT MODIFY", "=== DO NOT MODIFY ==="),
    ("IMPLEMENTATION REQUIREMENTS", "=== IMPLEMENTATION REQUIREMENTS ==="),
    ("ACCEPTANCE CRITERIA", "=== ACCEPTANCE CRITERIA ==="),
    ("EXECUTION INSTRUCTIONS", "=== EXECUTION INSTRUCTIONS ==="),
    ("IMPORTANT RULES", "=== IMPORTANT RULES ==="),
    ("OUTPUT FORMAT", "=== OUTPUT FORMAT (REQUIRED) ==="),
    ("COMPLETION SIGNAL", "=== COMPLETION SIGNAL ==="),
]

CRITICAL_SECTIONS = [
    "EXECUTION INSTRUCTIONS",
    "IMPORTANT RULES",
    "OUTPUT FORMAT",
    "COMPLETION SIGNAL",
]
```

Also verify the JSON output block exists:
```
grep -q '"task_completed"' "$file"
```

### 4. Report Results

#### Default Output (no --verbose)

```
Prompt Validation Report
========================

Directory: parallel/TS-0042-inventory/
Prompts found: 5

Results:
  task-001.txt: PASS
  task-002.txt: PASS
  task-003.txt: FAIL (missing: OUTPUT FORMAT, COMPLETION SIGNAL)
  task-004.txt: PASS
  task-005.txt: FAIL (missing: EXECUTION INSTRUCTIONS, IMPORTANT RULES, OUTPUT FORMAT, COMPLETION SIGNAL)

Summary:
  Passed: 3/5
  Failed: 2/5

Failed prompts are missing critical sections required for structured output.
Run with --fix to regenerate non-compliant prompts.
```

#### Verbose Output (--verbose)

```
Prompt Validation Report
========================

Directory: parallel/TS-0042-inventory/
Prompts found: 5

=== task-001.txt ===
  [✓] REQUIRED SKILLS
  [✓] CONTEXT
  [✓] OBJECTIVE
  [✓] CONTRACTS
  [✓] FILES TO CREATE
  [✓] FILES TO MODIFY
  [✓] DO NOT MODIFY
  [✓] IMPLEMENTATION REQUIREMENTS
  [✓] ACCEPTANCE CRITERIA
  [✓] EXECUTION INSTRUCTIONS
  [✓] IMPORTANT RULES
  [✓] OUTPUT FORMAT (REQUIRED)
  [✓] COMPLETION SIGNAL
  [✓] JSON output block
  Status: PASS

=== task-003.txt ===
  [✗] REQUIRED SKILLS
  [✓] CONTEXT
  [✓] OBJECTIVE
  [✓] CONTRACTS
  [✓] FILES TO CREATE
  [✓] FILES TO MODIFY
  [✓] DO NOT MODIFY
  [✓] IMPLEMENTATION REQUIREMENTS
  [✓] ACCEPTANCE CRITERIA
  [✗] EXECUTION INSTRUCTIONS        <- CRITICAL
  [✗] IMPORTANT RULES               <- CRITICAL
  [✗] OUTPUT FORMAT (REQUIRED)      <- CRITICAL
  [✗] COMPLETION SIGNAL             <- CRITICAL
  [✗] JSON output block
  Status: FAIL

...
```

### 5. Fix Mode (--fix)

If `--fix` is specified and there are failing prompts:

1. **Invoke the `parallel-prompt-generator` skill** to get the exact template
2. **Read the corresponding task file** from `tasks/task-NNN-*.md`
3. **Read context.md** for shared context
4. **Regenerate the prompt** using the skill template
5. **Backup the old prompt** to `prompts/task-NNN.txt.backup`
6. **Write the new prompt**

```
Fixing non-compliant prompts...

task-003.txt:
  Backup: prompts/task-003.txt.backup
  Reading: tasks/task-003-orders.md
  Regenerating with full template...
  Written: prompts/task-003.txt
  Status: FIXED

task-005.txt:
  Backup: prompts/task-005.txt.backup
  Reading: tasks/task-005-api.md
  Regenerating with full template...
  Written: prompts/task-005.txt
  Status: FIXED

Fixed: 2 prompts
Re-run validation to confirm: /parallel-validate-prompts $PARALLEL_DIR
```

### 6. Exit Codes

- `0`: All prompts valid
- `1`: Some prompts invalid (and --fix not specified)
- `2`: Directory not found or no prompts

---

## Examples

```bash
# Basic validation
/parallel-validate-prompts parallel/TS-0042-inventory/

# Detailed validation
/parallel-validate-prompts parallel/TS-0042-inventory/ --verbose

# Validate and fix non-compliant prompts
/parallel-validate-prompts parallel/TS-0042-inventory/ --fix

# Full verbose validation with fixes
/parallel-validate-prompts parallel/TS-0042-inventory/ --fix --verbose
```

## Common Issues

### Missing Critical Sections

**Cause**: Prompts generated by older tools or without using the `parallel-prompt-generator` skill.

**Solution**: Run with `--fix` to regenerate using the correct template.

### No JSON Output Block

**Cause**: The `=== OUTPUT FORMAT (REQUIRED) ===` section exists but doesn't contain the JSON template.

**Solution**: Regenerate with `--fix` or manually add:

```json
{
  "task_completed": boolean,
  "validation_passed": boolean,
  "files_created": [string],
  "files_modified": [string],
  "tests_run": integer,
  "tests_passed": integer,
  "tests_failed": integer,
  "summary": string,
  "full_log": string,
  "error_message": string | null
}
```

### Task File Not Found

**Cause**: Prompt file exists but corresponding task file in `tasks/` is missing.

**Solution**: Regenerate tasks with `/parallel-decompose` or create the missing task file manually.

---

## Related Commands

| Command | Purpose |
|---------|---------|
| `/parallel-decompose` | Generate tasks and prompts from Tech Spec |
| `/parallel-run` | Execute parallel agents (validates first) |
| `/parallel-integrate` | Verify integration after execution |

## Related Skills

| Skill | Purpose |
|-------|---------|
| `parallel-prompt-generator` | Template for generating prompts |
| `parallel-task-format` | Task file format specification |
