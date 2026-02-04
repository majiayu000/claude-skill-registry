---
name: validate
description: Verify implementation against acceptance criteria and run tests
argument-hint: <task ID or artifact path>
user-invocable: true
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
context: fork
agent: validator
---

# /validate - Implementation Validation

Verify that implementation meets acceptance criteria and passes tests.

## Purpose

Ensure quality by:
- Running test suites
- Checking acceptance criteria
- Validating artifact schemas
- Reporting findings

## Inputs

- `$ARGUMENTS`: Task ID or artifact path to validate
- BACKLOG for acceptance criteria: `docs/development/BACKLOG.md`
- PRD for requirements: `docs/architecture/PRD.md`
- `${PROJECT_NAME}`: Current project context

## Outputs

Validation report stored in Serena memory (transient).

## Workflow

### 1. Identify Target
Parse `$ARGUMENTS`:
- Task ID → Load task details and AC from BACKLOG
- File path → Validate specific artifact
- No args → Validate most recent implementation

### 2. Load Acceptance Criteria
From task details or PRD:
- List all criteria to check
- Note any dependencies

### 3. Run Tests
Execute appropriate test commands:
```bash
# Common patterns
npm test
pytest
make test
go test ./...
```

Capture results: passed, failed, skipped.

### 4. Verify Acceptance Criteria
For each criterion:
- Can it be verified automatically?
- If yes, run verification
- If no, check manually via code inspection

### 5. Check Quality
Run quality checks if available:
```bash
# Linting
npm run lint
ruff check .

# Type checking
tsc --noEmit
mypy .

# Format check
prettier --check .
ruff format --check .
```

### 6. Validate Artifacts
If artifacts were produced:
- Check schema compliance
- Verify required fields
- Validate references

### 7. Report Findings
Create validation report:

```yaml
---
date: YYYY-MM-DD
task: [Task ID]
target: [What was validated]
status: pass | fail | partial
---

## Summary
[Overall status and key findings]

## Test Results
| Suite | Passed | Failed | Skipped |
|-------|--------|--------|---------|
| [Name] | X | Y | Z |

## Acceptance Criteria
| ID | Criterion | Status | Evidence |
|----|-----------|--------|----------|
| AC1 | [Description] | Pass/Fail | [How verified] |

## Quality Checks
- [ ] Linting: [status]
- [ ] Type check: [status]
- [ ] Format: [status]

## Issues Found
1. [Issue description]
   - Severity: Low/Medium/High
   - Location: [file:line]

## Recommendation
[Pass/Fix issues/Block deployment]
```

## Validation Levels

### Quick Validation
- Run tests
- Check critical AC only
- Fast feedback

### Full Validation
- All tests
- All AC
- Quality checks
- Artifact validation

### Pre-Deploy Validation
- Full validation
- Security checks
- Performance baseline
- Integration tests

## Policy References

**Should-read** from `~/.claude/policy/RULES.md`:
- Failure Investigation - Root cause analysis, never skip tests or validation
