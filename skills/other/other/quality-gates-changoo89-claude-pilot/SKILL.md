---
name: quality-gates
description: Pre-commit quality validation procedures. Use when validating code quality before committing or in CI/CD.
---

# SKILL: Quality Gates

> **Purpose**: Pre-commit quality validation procedures (type-check, lint, todos, branch guard)
> **Target**: Coder Agent, pre-commit hooks, CI/CD pipelines

---

## Quick Start

### When to Use This Skill

- Before committing code (pre-commit hooks)
- Validating code quality in CI/CD
- Ensuring all todos complete before commit
- Preventing commits to protected branches

### Quick Reference

```bash
# Type check validation
npm run type-check  # or: tsc --noEmit

# Lint validation
npm run lint  # or: eslint . --ext .ts,.tsx

# Todo validation
/03_close  # Validates all SCs complete before closing plan

# Branch guard (Git native)
git config --global receive.denyDeleteCurrent warn
```

## Core Concepts

### Quality Gates Philosophy

**Pre-commit hooks** enforce quality standards before code enters the repository.

**Skills as procedures, hooks as automation**:
- Skills document the **what** and **how** (this file)
- Hooks execute the procedures automatically
- CI provides fallback enforcement
- Developer autonomy preserved (opt-in hooks)

**Why Opt-In Hooks?**
- Mandatory hooks improve baseline quality but create friction
- Skills + CI yields consistent enforcement while preserving autonomy
- Developers can choose strictness level (off/stop/strict profile)

## Procedures

### Type Check Validation

**Command**: `tsc --noEmit` or `npm run type-check`

**Output**: Success (exit 0) | Type errors with file/line (exit 1)

**Example Failure**: `src/auth/login.ts:15:11 - error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.`

### Lint Validation

**Command**: `npx eslint . --ext .ts,.tsx` or `npm run lint`

**Output**: Success (exit 0) | Lint errors with file/line/rule (exit 1)

**Example Failure**: `src/utils/format.ts:42:5  error  Unused vars  no-unused-vars`

### Todo Validation

**Command**: `/03_close`

**Steps**: Read plan → Check all SCs `[x]` → Verify evidence → Block if incomplete

**Example Block**: `⚠️  Incomplete SCs detected: - [ ] SC-3: Add unit tests (evidence missing)`

### Branch Guard

**Purpose**: Prevent accidental commits to protected branches

**Git Config**: `git config --global receive.denyDeleteCurrent warn`

**Pre-commit Hook**: Check if `CURRENT_BRANCH` in `main master develop` → exit 1 if protected

## Quality Gates Summary

| Gate | Command | Exit 0 | Exit 1 |
|------|---------|--------|--------|
| **Type Check** | `tsc --noEmit` | No type errors | Type errors found |
| **Lint** | `npm run lint` | No lint errors | Lint violations found |
| **Todos** | `/03_close` | All SCs complete | Incomplete SCs |
| **Branch Guard** | Pre-commit hook | Safe to commit | Protected branch |

## Integration Patterns

### Pre-commit Hook Setup

**Note**: Pre-commit hooks were removed in v4.4.14 as part of skill-based architecture migration. Use the docs-verify skill for documentation validation instead.

### CI/CD Integration

```yaml
# .github/workflows/quality.yml
jobs:
  quality:
    steps:
      - name: Type check
        run: npm run type-check
      - name: Lint
        run: npm run lint
      - name: Test
        run: npm test
```

## Troubleshooting

### Type Check Failures

**Causes**: Missing types `npm install --save-dev @types/node` | Incorrect tsconfig | Third-party types

**Debug**: `tsc --noEmit --listFiles` | `tsc --noEmit src/problem.ts`

### Lint Failures

**Solution**: Update `.eslintrc.js` rules or `// eslint-disable-next-line`

**Auto-fix**: `npx eslint . --fix`

## Best Practices

- **Run locally first**: Fix quality issues before pushing
- **Automate in CI**: Always run quality gates in CI/CD
- **Clear error messages**: Make failures easy to understand
- **Fast feedback**: Optimize for quick execution (<30s)
- **Graceful degradation**: Allow opting out with clear warnings

## Further Reading

**Internal**: @.claude/skills/quality-gates/REFERENCE.md - Complete hook scripts, CI/CD integration, troubleshooting | @.claude/skills/ralph-loop/SKILL.md - Quality gates in Ralph Loop

**External**: [Husky](https://github.com/typicode/husky) | [pre-commit](https://pre-commit.com/)
