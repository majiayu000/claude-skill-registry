---
name: Running Validation Loops
description: Execute self-correcting validation workflow. Use when validation fails, tests fail, or build breaks.
---

# Validation Loop

## When to Use
- npm run validate fails
- CI/CD breaks
- Test or build failures

## Process
1. Capture full error output
2. Analyze root cause in context of examples/
3. Apply minimal fix aligned with patterns
4. Re-run validation
5. Repeat until success (max 5 attempts)

## Commands
```bash
npm run validate
```

## Success Criteria
- All gates pass
- Fix follows patterns in examples/
- No new anti-patterns introduced