---
description: Verify documentation line numbers match current code state
---

# Context Engineering: Verify Documentation

Check if documentation line numbers still match the actual code.

## Purpose

After code changes, line numbers in documentation may drift. This skill:
1. Finds all `file:line` references in `.claude/` documentation
2. Verifies the referenced lines exist and match described content
3. Reports accuracy and suggests fixes

## Process

1. **Scan Documentation**
   - Find all patterns like `file.py:123` or `[file.py:123]`
   - Extract file path and line number

2. **Verify References**
   - Check if file exists
   - Check if line number is within file bounds
   - Sample content to verify it matches description

3. **Calculate Accuracy**
   - Total references found
   - Valid references
   - Accuracy percentage

4. **Generate Report**
   ```
   Documentation Accuracy Report
   =============================
   Total References: 156
   Valid: 142
   Invalid: 14
   Accuracy: 91%

   Invalid References:
   - context/workflows/auth.md:45 → src/auth.py:230 (line moved to 245)
   - context/workflows/api.md:12 → src/api.py:100 (file renamed)
   ```

## Usage

Check specific file:
```
/context-eng:verify-docs path/to/changed/file.py
```

Check all documentation:
```
/context-eng:verify-docs
```

Auto-fix (update line numbers):
```
/context-eng:verify-docs --fix
```

## Target Accuracy

| Level | Accuracy | Action |
|-------|----------|--------|
| Excellent | ≥80% | No action needed |
| Good | 60-80% | Update when convenient |
| Warning | 40-60% | Update soon |
| Critical | <40% | Update immediately |

## When to Run

- After refactoring
- After adding/removing significant code
- Before creating a PR
- Weekly maintenance
