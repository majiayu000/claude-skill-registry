---
name: ralph-qa
description: Manual QA validation trigger for RALPH implementations
allowed-tools: Bash, Read, Write, Glob, Grep, AskUserQuestion
---

# RALPH-QA - Manual Quality Assurance

Manually trigger QA validation on current implementation state.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-qa` | Run full QA validation against prd.json |
| `/ralph-qa --fix` | Attempt to fix found issues |
| `/ralph-qa --report` | Generate detailed QA report |
| `/ralph-qa US-001` | Validate specific story only |
| `/ralph-qa --history` | Show QA history and stats |

## Triggers

- `/ralph-qa`
- "run QA"
- "validate implementation"
- "check quality"

## Prerequisites

```bash
# Check for PRD
if [ ! -f prd.json ]; then
  echo "❌ No prd.json found"
  echo "Run /prd to create a PRD first"
  exit 1
fi

# Check for implementation plan (optional but helpful)
if [ -f implementation_plan.json ]; then
  echo "✓ Implementation plan found"
fi

# Check for config
if [ -f .ralph/config.yaml ]; then
  echo "✓ Config loaded"
fi
```

## QA Process

### Step 1: Load Context

Read all relevant context:

```bash
# Read PRD
cat prd.json | jq '.userStories[] | select(.passes == false)'

# Read implementation plan
cat implementation_plan.json 2>/dev/null

# Read QA history
cat .ralph/qa-history.json 2>/dev/null
```

### Step 2: Validate Acceptance Criteria

For each incomplete story, validate all acceptance criteria:

```
╔════════════════════════════════════════════════════════════════╗
║                    QA Validation                                ║
║                    Story: US-001                                ║
╚════════════════════════════════════════════════════════════════╝

Checking acceptance criteria...

✓ [1/5] Create User interface with required fields
  Evidence: Found in src/types/user.ts:5-15

✓ [2/5] Add Zod validation schema
  Evidence: Found in src/schemas/user.schema.ts:1-20

✗ [3/5] Export types from index.ts
  Issue: User type not exported
  File: src/types/index.ts

✓ [4/5] Add unit tests
  Evidence: Found tests/types/user.test.ts

✓ [5/5] Pass typecheck
  Evidence: npm run typecheck returns 0
```

### Step 3: Run Quality Gates

```bash
# From .ralph/config.yaml
npm run typecheck 2>&1
npm run lint 2>&1
npm test 2>&1
```

Output:

```
Quality Gates:
  ✓ Typecheck: passed (0 errors)
  ✓ Lint: passed (2 warnings)
  ✓ Tests: passed (42/42, 8 new)

Coverage:
  Statements: 87%
  Branches: 82%
  Functions: 91%
  Lines: 87%
```

### Step 4: Check Code Quality

Additional code quality checks:

```
Code Quality:
  ✓ No TODO comments in new code
  ✓ No console.log statements
  ✓ Error handling present
  ⚠ Missing JSDoc on 2 functions
  ✓ No hardcoded secrets
```

### Step 5: Generate Report

```
╔════════════════════════════════════════════════════════════════╗
║                    QA Report                                    ║
╚════════════════════════════════════════════════════════════════╝

Stories Validated: 3
  ✓ US-001: Create User model (5/5 criteria)
  ✓ US-002: Password hashing (4/4 criteria)
  ✗ US-003: JWT utilities (3/5 criteria)

Overall Status: NEEDS_FIX

Issues Found: 2
  [HIGH] Missing export in src/types/index.ts
  [LOW] Missing JSDoc in src/utils/jwt.ts

Quality Gates: ALL PASS
  ✓ Typecheck
  ✓ Lint
  ✓ Tests

Recommendations:
  1. Add export statement for User type
  2. Add JSDoc to jwt utility functions
```

## Fix Mode

With `/ralph-qa --fix`:

```
╔════════════════════════════════════════════════════════════════╗
║                    QA Fix Mode                                  ║
╚════════════════════════════════════════════════════════════════╝

Issues to fix: 2

[1/2] Missing export in src/types/index.ts
  Status: AUTO-FIXABLE
  Action: Adding export statement...
  ✓ Fixed

[2/2] Missing JSDoc in src/utils/jwt.ts
  Status: REQUIRES MANUAL FIX
  Suggestion: Add JSDoc comments to verifyToken() and signToken()

Fix Results:
  ✓ Fixed: 1
  ○ Manual: 1

Re-running validation...
  ✓ All auto-fixable issues resolved
  ⚠ 1 issue requires manual attention
```

## Detailed Report Mode

With `/ralph-qa --report`:

Generates comprehensive report to `.ralph/qa-report.json`:

```json
{
  "generatedAt": "2026-01-25T10:30:00Z",
  "summary": {
    "storiesValidated": 3,
    "storiesPassed": 2,
    "storiesFailed": 1,
    "criteriaTotal": 14,
    "criteriaPassed": 12,
    "criteriaFailed": 2
  },
  "stories": [
    {
      "id": "US-001",
      "title": "Create User model",
      "status": "passed",
      "criteria": [
        {"criterion": "...", "passed": true, "evidence": "..."}
      ]
    }
  ],
  "qualityGates": {
    "typecheck": {"status": "passed", "output": "..."},
    "lint": {"status": "passed", "warnings": 2},
    "tests": {"status": "passed", "total": 42, "passed": 42}
  },
  "issues": [...],
  "recommendations": [...]
}
```

## History Mode

With `/ralph-qa --history`:

```
╔════════════════════════════════════════════════════════════════╗
║                    QA History                                   ║
╚════════════════════════════════════════════════════════════════╝

QA Sessions: 12

Recent Sessions:
  [2026-01-25 10:30] US-003 - FAILED (2 issues)
  [2026-01-25 09:15] US-002 - PASSED (1st attempt)
  [2026-01-25 08:00] US-001 - PASSED (3 attempts)

Statistics:
  Success Rate: 83%
  Avg Attempts: 1.5
  Total Issues Found: 8
  Issues Auto-Fixed: 5
  Issues Manual-Fixed: 3

Recurring Issues:
  ⚠ Missing exports (3 occurrences)
  ⚠ Missing JSDoc (2 occurrences)

Insights Logged: 5
  - "Always export new types from index.ts"
  - "Use Zod for runtime validation"
  - ...
```

## Integration with QA Loop

This skill uses the `qa-loop.js` module:

```javascript
// Functions available from qa-loop.js
runQaValidation(subtask, implementation)
runQaFix(issues, context)
escalateToHuman(issues, subtask, attempts)
getQaStats(projectRoot)
createQaSession(subtaskId, projectRoot)
```

## Output Formats

### Console Output (Default)

```
╔══════════════════════════════════════╗
║          QA VALIDATION               ║
╚══════════════════════════════════════╝

Status: PASSED
Stories: 3/3
Criteria: 14/14

✓ All acceptance criteria met
✓ All quality gates pass

No issues found.
```

### JSON Output (--json flag)

```json
{
  "status": "passed",
  "stories": {"total": 3, "passed": 3},
  "criteria": {"total": 14, "passed": 14},
  "issues": [],
  "timestamp": "2026-01-25T10:30:00Z"
}
```

## Error Handling

| Error | Action |
|-------|--------|
| No PRD found | Direct to `/prd [feature]` |
| No config | Use default quality commands |
| Quality gate fails | Report and offer fix mode |
| Tests fail | Show test output, suggest fixes |
| Fix fails | Log and suggest manual fix |

## Guidelines

1. **BE THOROUGH** - Check every criterion explicitly
2. **SHOW EVIDENCE** - Prove where criteria are satisfied
3. **CLEAR ISSUES** - Make fix instructions actionable
4. **TRACK HISTORY** - Log all sessions and learnings
5. **OFFER FIXES** - Auto-fix when safe, suggest for others
