---
name: shared-validation-feedback-loops
description: Type-check, lint, test, build validation sequence. Use proactively before every commit across all agents.
category: validation
---

# Feedback Loops

> "Validate early, validate often – catch errors before they compound."

## When to Use This Skill

Use **before every task related changes commit** to ensure code quality and prevent broken builds.

## Quick Start

**⚠️ PRE-REQUISITE: Test Coverage Check (BLOCKING)**

Before running feedback loops, verify test coverage exists:

```bash
# Check for modified files without tests
git diff --name-only HEAD~5 | grep '^src/' | while read file; do
  test_file="src/tests/${file#src/}"
  test_file="${test_file%.ts}.test.ts"
  if [ ! -f "$test_file" ]; then
    echo "COVERAGE GAP: $file missing $test_file"
  fi
done

# If coverage gaps found: BLOCK - invoke test-creator
```

**Then run all feedback loops in sequence:**

```bash
npm run type-check && npm run lint && npm run build  && npm run test && npm run test:e2e
```

## Test Coverage Gate (Before Feedback Loops)

**⚠️ BLOCKING CHECK: Tests must exist for modified code.**

```bash
# For each source file modified, verify test exists:
src/components/game/player/index.ts → src/tests/components/game/player/index.test.ts
src/services/ShootingService.ts → src/tests/services/ShootingService.test.ts

# If tests missing: BLOCK and invoke test-creator
Task({
  subagent_type: "test-creator",
  description: "Create tests for missing coverage",
  prompt: "Create unit/E2E tests for: {files_missing_coverage}"
})
```

**If tests fail:**

1. Read the failure message carefully
2. Check which test failed
3. Review recent changes that could affect it
4. Fix the code (not the test, unless test is wrong)
5. Commit changes and merge

**Common Issues:**

- Import errors not caught by tsc
- Missing environment variables
- Bundle size issues
- Asset loading problems

## Decision Framework

| Step       | Time | What It Catches               |
| ---------- | ---- | ----------------------------- |
| type-check | ~5s  | Type errors, missing imports  |
| lint       | ~3s  | Style issues, potential bugs  |
| test       | ~10s | Logic errors, regressions     |
| build      | ~30s | Bundle issues, runtime errors |

## When to Skip Steps

| Situation         | What to Run                                 |
| ----------------- | ------------------------------------------- |
| Small type change | type-check only (then full before commit)   |
| Styling only      | lint only (then full before commit)         |
| Quick iteration   | type-check + lint (then full before commit) |
| **Before commit** | **Always run ALL four**                     |

## Anti-Patterns

❌ **DON'T:**

- Commit without running feedback loops
- Use `@ts-ignore` or `// eslint-disable` to hide errors
- Skip tests because "it's a small change"
- Use `any` type without justification
- Comment out failing tests

✅ **DO:**

- Run all loops before every commit
- Fix errors properly, don't suppress
- Update tests when behavior changes
- Add types to all public interfaces
- Run `--fix` for auto-fixable issues

**Load State Decision Tree:**

- `domcontentloaded` - Use by default. Fastest, most reliable.
- `load` - Use when testing images, fonts, or media loading.
- `networkidle` - Rare. Only for SPAs with continuous polling.

**Lesson from bugfix-e2e-001:** Changing `networkidle` to `domcontentloaded` fixed timeout issues. 23/23 accessibility tests now pass.

### Server Port Management

**Lesson from bugfix-e2e-002:** Explicit port cleanup prevents EADDRINUSE errors. 65/65 E2E tests passing (100% success rate).
