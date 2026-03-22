---
name: codebase-quality:code-quality
description: Code quality analysis including linting, style, type safety, and refactoring suggestions. Use when checking code style, running linters, analyzing complexity, or suggesting refactoring. Invoked by codebase-quality:full-audit after security passes. Triggers on lint, code style, type check, refactor, code quality, complexity.
version: 1.0.0
title: "Codebase Quality:Code Quality"
status: active
---

# Code Quality Sub-Skill

Part of the [codebase-quality](../using-codebase-quality/SKILL.md) skill family.

## Purpose

Analyze and improve code quality through linting, type checking, style enforcement, and complexity analysis.

## Prerequisites

**Run security first**: `Skill("codebase-quality:security")`

This ensures security issues are addressed before style fixes that might obscure vulnerabilities.

## Quick Reference

### Commands

```bash
# Full code quality check
/codebase-quality code

# Specific checks
/codebase-quality lint
/codebase-quality types
/codebase-quality style
/codebase-quality complexity
```

### Invocation

```python
# From wrapper skill
Skill("codebase-quality:code-quality")

# After quality complete, chain to docs
Skill("codebase-quality:documentation")
```

## Quality Checks

### 1. Linting

**Frontend (TypeScript/React)**:
```bash
cd my-project-frontend && npm run lint
```

**Backend (Python)**:
```bash
cd my-project-backend && ruff check .
```

**Severity Levels**:
| Level | Action |
|-------|--------|
| Error | Must fix before merge |
| Warning | Should fix, not blocking |
| Info | Suggestion only |

### 2. Type Safety

**Frontend (TypeScript)**:
```bash
cd my-project-frontend && npm run build:dev
# or
npx tsc --noEmit
```

**Backend (Python)**:
```bash
cd my-project-backend && mypy .
```

**Common Issues**:
- `any` type usage (prefer explicit types)
- Missing return types
- Nullable without handling
- Implicit type coercion

### 3. Style Consistency

**Checked Elements**:
- Import ordering
- Naming conventions (camelCase vs snake_case)
- File organization
- Comment formatting
- Whitespace and indentation

**Formatters**:
```bash
# Frontend
npm run format  # Prettier

# Backend
ruff format .
```

### 4. Complexity Analysis

**Metrics**:
- Cyclomatic complexity (max 10 per function)
- Function length (max 50 lines)
- File length (max 500 lines)
- Nesting depth (max 4 levels)

**Detection**:
```bash
# Python
radon cc . -a  # Cyclomatic complexity

# JavaScript/TypeScript
npx eslint . --rule 'complexity: ["warn", 10]'
```

## Quality Report Format

```markdown
# Code Quality Report - 2025-12-19

## Summary
- **Files Analyzed**: 45
- **Issues Found**: 12
- **Severity**: 3 errors, 7 warnings, 2 info

## Errors (Must Fix)

### E001: Type Error in ChatInterface.tsx:45
```typescript
// Current: missing type annotation
const data = response.json()

// Fix: add explicit type
const data: ChatResponse = await response.json()
```

### E002: Lint Error in agent.py:123
```python
# Current: unused import
from typing import Any, Optional

# Fix: remove unused
from typing import Optional
```

## Warnings (Should Fix)

### W001: High Complexity in process_message():92
- Cyclomatic complexity: 15 (max: 10)
- Recommendation: Extract sub-functions

### W002: Long File vector_search.py
- Lines: 623 (max: 500)
- Recommendation: Split into modules

## Passed Checks

✅ All imports sorted correctly
✅ Naming conventions consistent
✅ No debug statements in production code
✅ All functions have docstrings (Python)
```

## Automatic Fixes

### Safe Auto-Fixes

```bash
# Apply safe formatting fixes
npm run format --write       # Frontend
ruff format . --fix          # Backend

# Auto-fix safe lint issues
npm run lint -- --fix        # Frontend
ruff check . --fix           # Backend
```

### Manual Fixes Required

- Complex refactoring
- Type annotation changes
- Logic restructuring
- API signature changes

## Integration with Workflow

### In codebase-quality:full-audit

```
codebase-quality:security
    ↓ (passes)
codebase-quality:code-quality  ← YOU ARE HERE
    ↓
1. Run linters
2. Run type checkers
3. Analyze complexity
4. Generate report
5. Apply safe auto-fixes
    ↓
If errors: Report and stop
If warnings only: Continue with warnings
    ↓
codebase-quality:documentation
```

### In Pre-Merge Check

```
/codebase-quality pre-merge
    ↓
code-quality check:
- Errors → Block merge
- Warnings → Allow with notice
- Info → Allow silently
```

## Best Practices

1. **Run Before Commit**: Always run linters before committing
2. **Auto-Format**: Use formatters for consistent style
3. **Type Everything**: Avoid `any` in TypeScript
4. **Keep Functions Small**: Extract complex logic into helpers
5. **Review Warnings**: Don't ignore warnings indefinitely

## Chaining

After code quality passes or warns:

```python
# Continue to documentation update
Skill("codebase-quality:documentation")
```

If code quality has blocking errors:

```python
# Fix errors first, then re-run
# Do NOT proceed to documentation until clean
```

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-19
**Parent Skill**: [using-codebase-quality](../using-codebase-quality/SKILL.md)
