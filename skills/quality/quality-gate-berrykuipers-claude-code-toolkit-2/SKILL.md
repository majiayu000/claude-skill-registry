---
name: quality-gate
description: Comprehensive quality validation for TypeScript/JavaScript projects - runs TypeScript checks, tests, coverage analysis, build validation, and linting with structured JSON results
---

# Quality Gate

Complete quality validation workflow for TypeScript/JavaScript projects. Executes all quality checks and returns structured results.

## Purpose

Execute comprehensive quality validation before code can proceed to PR creation, ensuring all quality standards are met through automated checks and minimum thresholds.

## Quality Standards

All checks must pass:
- ✅ TypeScript type checking (no errors)
- ✅ Linting validation (no errors, warnings acceptable)
- ✅ All tests passing
- ✅ Test coverage ≥ 80% (configurable)
- ✅ Production build successful

## Usage

This skill runs the Python script `skill.py` which executes all quality checks.

### Parameters

- `project_path`: Absolute path to the project directory
- `coverage_threshold`: Minimum coverage percentage (default: 80)

### Example

```python
# In Claude conversation or API
result = use_skill("quality-gate", {
    "project_path": "/path/to/your/project",
    "coverage_threshold": 80
})

if result["qualityGate"] == "pass":
    # All checks passed, proceed to PR creation
    print("✅ Quality gate passed!")
else:
    # Show blockers
    for blocker in result["blockers"]:
        print(f"❌ {blocker}")
```

## Output Format

Returns structured JSON:

```json
{
  "qualityGate": "pass" | "fail",
  "timestamp": "2025-10-22T...",
  "checks": {
    "typeCheck": {
      "status": "pass",
      "errors": 0
    },
    "lint": {
      "status": "pass",
      "errors": 0,
      "warnings": 2
    },
    "tests": {
      "status": "pass",
      "total": 45,
      "passed": 45,
      "failed": 0,
      "coverage": 87.5
    },
    "build": {
      "status": "pass",
      "duration": "12.3s",
      "warnings": 0
    }
  },
  "blockers": [],
  "warnings": ["2 lint warnings"]
}
```

## Implementation

The skill executes checks in this order:
1. TypeScript type checking (fast, catches syntax errors)
2. Linting (fast, catches style issues)
3. Tests with coverage (slower, comprehensive validation)
4. Production build (final validation)

Fast-failing approach ensures quick feedback.

## Integration with Conductor

Used in Conductor Phase 3 (Quality Assurance):

```markdown
**Phase 3: Quality Assurance**

Use `quality-gate` API skill:
1. Execute quality gate with project path
2. If pass: Proceed to Phase 4 (PR Creation)
3. If fail:
   - Identify failing check
   - Route to appropriate agent for fixes
   - Re-run quality gate
```

## When to Use

- Conductor workflow Phase 3 (Quality Assurance)
- Before creating any pull request
- After refactoring changes
- As part of CI/CD pipeline
- Before merging to development branch

## Failure Handling

If quality gate fails:
1. Check `blockers` array for specific issues
2. Route to appropriate agent:
   - TypeScript errors → Fix type issues
   - Lint errors → Auto-fix with `npm run lint -- --fix`
   - Tests fail → Debugger agent
   - Build fails → Investigate build errors
3. Re-run quality gate after fixes
4. Maximum 3 retries before escalating to human
