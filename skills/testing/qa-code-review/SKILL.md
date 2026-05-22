---
name: qa-code-review
description: Code quality review before validation. Checks for @ts-ignore, any types, anti-patterns, and potential issues. Use proactively at start of QA validation.
category: validation
user-invocable: true
---

# QA Code Review

> "Review code quality BEFORE running automated checks - catch issues early."

Review code quality before running type-check, lint, test, and build. This catches issues that automated tools might miss and ensures code quality standards are met.

## When to Use

Use at the start of validation, before type-check/lint/test/build loops.

## Quality Checks

| Check | Pattern | Severity | Action if Found |
|-------|---------|----------|-----------------|
| TypeScript suppressions | `@ts-ignore`, `@@ts-expect-error` | **HIGH** | FAIL - Report location |
| Any types | `: any`, `<any>`, `as any` | **HIGH** | FAIL - Report location |
| Missing dependencies | `useEffect` without deps | **HIGH** | FAIL - Report location |
| State mutations | Direct object/array mutation | **HIGH** | FAIL - Report location |
| Memory leaks | Event listeners without cleanup | **HIGH** | FAIL - Report location |
| Console logs | `console.log`, `console.error` | **MEDIUM** | WARN - Report location |
| Debug flags | `debug &&`, `DEBUG &&` | **MEDIUM** | FAIL - May hide features |
| Empty catch blocks | `catch {}` with no handling | **MEDIUM** | FAIL - Swallows errors |
| TODO comments | `TODO`, `FIXME` in production code | **LOW** | NOTE - Track separately |

## Process

1. **Identify changed files** from the task
2. **Grep** for anti-patterns across changed files
3. **Read** each changed file to review context
4. **Check** for quality issues using the table above
5. **Report** findings with specific file locations and line numbers

## Grep Patterns for Code Review

```bash
# TypeScript suppressions
grep -r "@ts-ignore\|@ts-expect-error" src/

# Any types
grep -r ": any\|<any>\|as any" src/

# Missing dependencies (manual review needed)
grep -r "useEffect" src/ | grep -v "useEffect(("

# Console logs
grep -r "console\." src/

# Empty catch blocks
grep -r "catch {}" src/

# TODO comments
grep -r "TODO\|FIXME" src/
```

## Output Format

```markdown
## Code Review Results

### Files Reviewed
- {file1.ts}
- {file2.tsx}
- {file3.ts}

### Issues Found

{If issues found:}
| Severity | File | Line | Issue | Suggestion |
|----------|------|------|-------|------------|
| high | src/file.ts | 42 | @ts-ignore used | Remove suppression, fix type error |
| high | src/components/Button.tsx | 15 | : any type | Add proper type annotation |
| medium | src/utils/helpers.ts | 78 | console.log left | Remove before commit |

{If no issues:}
**No quality issues found.** Code is ready for automated validation.

### Overall Result
- Status: ✅ PASS / ❌ FAIL

### Notes
{Additional observations or concerns}
```

## Decision Framework

| Issue Count | Action |
|-------------|--------|
| 0 high/medium issues | PASS - Proceed to validation |
| 1+ high-severity | FAIL - Fix required before validation |
| 1+ medium-severity | FAIL - Fix recommended |
| Low-severity only | PASS - Note in report |

## Important

- Report exact file paths and line numbers
- Suggest specific fixes for each issue
- If ANY high-severity issue found, overall result is FAIL
- Console warnings are considered failures
- Check for debug flags that may hide features from users
- Be thorough - missed issues become bugs later

## Code Quality Fail Criteria

**This is the definitive fail criteria list. If ANY of these are found, validation must FAIL:**

- Any `any` type usage (without explicit justification)
- Any `@ts-ignore` or `@ts-expect-error` comments
- Missing React hook dependencies
- Direct state mutations
- Memory leaks (event listeners not cleaned up)
- Empty catch blocks that swallow errors
- Debug flags that disable features
- Console errors or warnings
- Lint warnings of any kind

**Note**: Console warnings and lint warnings are considered FAIL conditions.

## See Also

- [qa-validation-workflow](../qa-validation-workflow/SKILL.md) — Full validation pipeline
- [dev-validation-quality-gates](../dev-validation-quality-gates/SKILL.md) — Quality gate standards
