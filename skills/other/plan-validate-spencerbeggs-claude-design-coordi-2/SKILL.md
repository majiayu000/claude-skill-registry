---
name: plan-validate
description: Validate plan document structure and frontmatter. Use when checking plans for compliance, ensuring proper formatting, or verifying metadata before commits.
allowed-tools: Read, Bash
agent: design-doc-agent
---

# Plan Validation

Validates plan documentation files for structure, frontmatter, and quality
compliance.

## Overview

This skill validates plan documents by:

1. Reading the plan configuration from design.config.json
2. Finding plan files for validation
3. Validating YAML frontmatter structure and values
4. Checking required fields and data types
5. Validating status-progress alignment
6. Validating dates and field relationships
7. Reporting issues with actionable recommendations

## Quick Start

**Validate specific plan:**

```bash
/plan-validate plan-design-linking-phase-1
```

**Validate all plans:**

```bash
/plan-validate --all
```

**Validate with strict mode:**

```bash
/plan-validate plan-design-linking-phase-1 --strict
```

## How It Works

### 1. Parse Parameters

- `plan-name`: Plan name/ID to validate (or --all for all plans) [REQUIRED]
- `--strict`: Enable strict mode with additional quality checks
- `--fix`: Auto-fix issues when possible

### 2. Load Configuration

Read `.claude/design/design.config.json` to get:

- Plan paths and directories
- Quality standards for plans
- Required frontmatter fields
- Valid status values
- Progress range limits

### 3. Locate Plan File

Use the plan name to find the file:

- Check `.claude/plans/{plan-name}.md`
- If not found, check `.claude/plans/_archive/{plan-name}.md`
- Report error if file doesn't exist

### 4. Validate Plan Document

Execute `scripts/validate-plan.sh` (co-located with this skill) which checks:

**Required Fields:**

- name (kebab-case format)
- title (non-empty string)
- created (YYYY-MM-DD format)
- status (valid enum value)
- progress (0-100 integer)

**Status Values:**

- ready
- in-progress
- blocked
- completed
- abandoned

**Status-Progress Alignment:**

- ready: progress must be 0%
- in-progress/blocked: progress 1-99%
- completed: progress must be 100%

**Date Validation:**

- All dates in YYYY-MM-DD format
- created ≤ updated
- started ≤ completed (if both present)

**Completion Requirements:**

- Status completed: requires completed date and outcome
- Status abandoned: requires completed date and archival-reason

**Optional Field Validation:**

- modules: must exist in design.config.json
- implements: paths must point to existing design docs
- phases: each phase has required fields (name, status, progress)

### 5. Generate Report

Output validation results:

**Success:**

```text
✓ Plan validation passed: plan-design-linking-phase-1
  ✓ All required fields present
  ✓ Status-progress aligned (ready, 0%)
  ✓ Dates valid and in order
  ✓ No issues found
```

**Failure:**

```text
✗ Plan validation failed: plan-design-linking-phase-1

Errors (3):
  ✗ Missing required field: status
  ✗ progress: 150 (must be integer 0-100)
  ✗ Status 'completed' requires 'outcome' field

Warnings (1):
  ⚠ Status 'ready' should have progress 0%, found 25%
```

## Usage Patterns

### Validate Before Commit

```bash
# Check plan before committing
/plan-validate my-feature-plan
```

### Validate All Plans

```bash
# Check entire plan directory
/plan-validate --all
```

### Fix Common Issues

```bash
# Auto-fix when possible (updates dates, formats fields)
/plan-validate my-feature-plan --fix
```

### Strict Validation

```bash
# Additional quality checks
/plan-validate my-feature-plan --strict
```

Strict mode adds:

- Check for stale plans (no updates >30 days)
- Verify bidirectional links to design docs
- Check for orphaned plans (no implements field)
- Validate estimated vs actual effort alignment

## Implementation Steps

1. **Parse arguments** from user input (plan name, flags)
2. **Read config** from `.claude/design/design.config.json`
3. **Locate plan file** in `.claude/plans/` or `_archive/`
4. **Execute validation script** `scripts/validate-plan.sh`
5. **Parse script output** to extract errors/warnings
6. **Check additional rules** if strict mode enabled
7. **Generate report** with colored output and recommendations
8. **Return exit code** (0 = pass, 1 = fail)

## Error Messages

### Missing Required Fields

```text
✗ Missing required field: {field}

Fix: Add '{field}: value' to the plan frontmatter
```

### Invalid Status Value

```text
✗ status: '{value}' (must be one of: ready, in-progress, blocked,
  completed, abandoned)

Fix: Change status to a valid value
```

### Status-Progress Mismatch

```text
⚠ Status 'ready' should have progress 0%, found {value}%

Fix: Either set progress to 0 or change status to 'in-progress'
```

### Invalid Date Format

```text
✗ {field}: {value} (must be YYYY-MM-DD)

Fix: Use format YYYY-MM-DD (e.g., 2026-01-18)
```

### Missing Completion Fields

```text
✗ Status 'completed' requires 'outcome' field

Fix: Add 'outcome: success|partial|failed' to frontmatter
```

## Examples

See [examples.md](./examples.md) for detailed usage examples.

## Related Skills

- `plan-create` - Create new plans
- `plan-update` - Update plan status/progress
- `plan-list` - List all plans
- `design-validate` - Validate design docs
