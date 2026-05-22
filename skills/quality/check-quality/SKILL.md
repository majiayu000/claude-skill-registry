---
name: check-quality
description: |
  Audit quality gates: tests, CI/CD, hooks, coverage, linting.
  Outputs structured findings. Use log-quality-issues to create issues.
  Invoke for: quality infrastructure audit, test coverage gaps, CI review.
---

# /check-quality

Audit quality infrastructure. Output findings as structured report.

## What This Does

1. Check testing infrastructure (Vitest, Jest, coverage)
2. Check git hooks (Lefthook, Husky)
3. Check CI/CD (GitHub Actions)
4. Check linting/formatting (ESLint, Prettier, Biome)
5. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-quality-issues` to create GitHub issues or `/fix-quality` to fix.

## Process

### 1. Testing Infrastructure

```bash
# Test runner
[ -f "vitest.config.ts" ] || [ -f "vitest.config.js" ] && echo "✓ Vitest" || echo "✗ Vitest"
[ -f "jest.config.ts" ] || [ -f "jest.config.js" ] && echo "✓ Jest" || echo "✗ Jest (prefer Vitest)"

# Coverage
grep -q "coverage" package.json 2>/dev/null && echo "✓ Coverage script" || echo "✗ Coverage script"
grep -q "@vitest/coverage" package.json 2>/dev/null && echo "✓ Coverage plugin" || echo "✗ Coverage plugin"

# Test files exist
find . -name "*.test.ts" -o -name "*.spec.ts" 2>/dev/null | head -5 | wc -l | xargs -I{} echo "{} test files found"
```

### 2. Git Hooks

```bash
# Hook manager
[ -f "lefthook.yml" ] && echo "✓ Lefthook" || echo "✗ Lefthook (recommended)"
[ -f ".husky/_/husky.sh" ] && echo "✓ Husky (prefer Lefthook)" || echo "- Husky not found"

# Hooks installed
[ -f ".git/hooks/pre-commit" ] && echo "✓ pre-commit hook" || echo "✗ pre-commit hook"
[ -f ".git/hooks/pre-push" ] && echo "✓ pre-push hook" || echo "✗ pre-push hook"
```

### 3. CI/CD

```bash
# GitHub Actions
[ -f ".github/workflows/ci.yml" ] || [ -f ".github/workflows/test.yml" ] && echo "✓ CI workflow" || echo "✗ CI workflow"

# CI coverage reporting
grep -rq "vitest-coverage-report" .github/workflows/ 2>/dev/null && echo "✓ Coverage in PRs" || echo "✗ Coverage in PRs"

# Branch protection (check via gh)
gh api repos/{owner}/{repo}/branches/main/protection 2>/dev/null | jq -r '.required_status_checks.contexts[]?' 2>/dev/null | head -3
```

### 4. Linting & Formatting

```bash
# ESLint
[ -f "eslint.config.js" ] || [ -f ".eslintrc.js" ] || [ -f ".eslintrc.json" ] && echo "✓ ESLint" || echo "✗ ESLint"

# Prettier
[ -f "prettier.config.js" ] || [ -f ".prettierrc" ] && echo "✓ Prettier" || echo "- Prettier not found"

# Biome (modern alternative)
[ -f "biome.json" ] && echo "✓ Biome" || echo "- Biome not found"

# TypeScript
[ -f "tsconfig.json" ] && echo "✓ TypeScript" || echo "✗ TypeScript"
grep -q '"strict": true' tsconfig.json 2>/dev/null && echo "✓ Strict mode" || echo "✗ Strict mode"
```

### 5. Commit Standards

```bash
# Commitlint
[ -f "commitlint.config.js" ] || [ -f "commitlint.config.cjs" ] && echo "✓ Commitlint" || echo "✗ Commitlint"

# Changesets
[ -d ".changeset" ] && echo "✓ Changesets" || echo "- Changesets not found"
```

### 6. Test Coverage Analysis

```bash
# Run coverage if available
pnpm coverage 2>/dev/null | tail -20 || npm run coverage 2>/dev/null | tail -20 || echo "No coverage script"
```

Spawn `test-strategy-architect` agent for deep test quality analysis if tests exist.

## Output Format

```markdown
## Quality Gates Audit

### P0: Critical (Must Have)
- No test runner configured - Cannot verify code works
- No CI workflow - Changes not validated before merge

### P1: Essential (Every Project)
- No pre-commit hooks - Code can be committed without checks
- No coverage configured - Cannot measure test coverage
- ESLint not configured - No static analysis
- TypeScript not in strict mode - Losing type safety

### P2: Important (Production Apps)
- No commitlint - Inconsistent commit messages
- No coverage reporting in PRs - Hard to track test quality
- No pre-push hooks - Tests bypass possible

### P3: Nice to Have
- Consider Lefthook over Husky (faster, simpler)
- Consider Vitest over Jest (faster, native ESM)
- Consider Biome over ESLint+Prettier (faster, unified)

## Current Status
- Test runner: None
- Coverage: Not configured
- Git hooks: None
- CI/CD: None
- Linting: Partial

## Summary
- P0: 2 | P1: 4 | P2: 3 | P3: 3
- Recommendation: Set up Vitest with Lefthook hooks first
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No test runner | P0 |
| No CI workflow | P0 |
| No coverage | P1 |
| No git hooks | P1 |
| No linting | P1 |
| Not strict TypeScript | P1 |
| No commitlint | P2 |
| No coverage in PRs | P2 |
| Tool upgrades | P3 |

## Related

- `/log-quality-issues` - Create GitHub issues from findings
- `/fix-quality` - Fix quality infrastructure
- `/quality-gates` - Full quality setup workflow
