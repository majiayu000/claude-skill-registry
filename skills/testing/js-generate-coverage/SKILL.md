---
name: js-generate-coverage
description: Self-contained command for coverage generation and analysis
user-invocable: true
allowed-tools: Skill, Read, Glob, Grep, Bash
---

# JavaScript Coverage Report Skill

Self-contained skill that generates test coverage reports and analyzes results.

## Parameters

- **files** - (Optional) Specific files to check coverage for
- **workspace** - (Optional) Workspace name for monorepo projects

## Usage Examples

```
/js-generate-coverage
/js-generate-coverage workspace=frontend
/js-generate-coverage files=src/utils/validator.js
```

## Workflow

### Step 1: Generate Coverage

**Execute npm coverage command:**
```bash
npm run test:coverage > target/npm-coverage-output.log 2>&1
# Or with workspace:
npm run test:coverage --workspace={workspace} > target/npm-coverage-output.log 2>&1
```

**Parse build output (if needed):**
```bash
python3 .plan/execute-script.py pm-dev-frontend:cui-javascript-project:npm-output parse-npm-output \
    --log target/npm-coverage-output.log --mode structured
```

This generates coverage reports in coverage/ directory.

### Step 2: Analyze Coverage

**Load skill and execute workflow:**
```
Skill: pm-dev-frontend:js-implement-tests
Execute workflow: Analyze Coverage
```

Or run script directly:
```bash
python3 .plan/execute-script.py pm-dev-frontend:js-implement-tests:js-coverage analyze --report coverage/coverage-summary.json
# Or for LCOV format:
python3 .plan/execute-script.py pm-dev-frontend:js-implement-tests:js-coverage analyze --report coverage/lcov.info --format lcov
```

Script returns structured JSON with overall_coverage, by_file, and low_coverage_files.

### Step 3: Return Coverage Results

```json
{
  "overall_coverage": {
    "line_coverage": 87.3,
    "branch_coverage": 82.1
  },
  "low_coverage_files": [...],
  "summary": {...}
}
```

## Related

- Skill: `pm-dev-frontend:js-implement-tests` - Analyze Coverage workflow
- Skill: `pm-dev-frontend:cui-javascript-project` - Parse npm Build Output workflow
- Skill: `/js-implement-tests` - Add tests for low-coverage areas
