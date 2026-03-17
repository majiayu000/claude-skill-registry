---
description: Run a comprehensive code quality check looking for common patterns that AI coding agents introduce.
---

# Vibe Check

Run a comprehensive code quality check on the current codebase, looking for common patterns that AI coding agents introduce.

## Instructions

Analyze the codebase for the following issues. For each category, search the relevant file types and report what you find.

### 1. Debug Statements
Search for debug statements that shouldn't go to production:
- Python: `print()`, `breakpoint()`, `pdb.set_trace()`, `ipdb`
- JS/TS: `console.log()`, `console.debug()`, `console.info()`, `debugger`

Ignore: `console.error()`, `console.warn()`, `logger.*` calls, and lines with `// noqa: debug` or `# noqa: debug`

### 2. TODO/FIXME Comments
Search for unfinished work markers:
- `TODO`, `FIXME`, `XXX`, `HACK`, `BUG`

Skip markdown files and dedicated TODO files.

### 3. Empty Catch Blocks
Search for error handling that silently swallows errors:
- Python: `except: pass` or `except Exception: pass`
- JS/TS: `catch (e) {}` or `.catch(() => {})`

### 4. Hardcoded URLs
Search for localhost/development URLs:
- `http://localhost:`
- `http://127.0.0.1:`

Skip test files and config files.

### 5. snake_case in TypeScript
Search TypeScript interface/type definitions for snake_case property names that should be camelCase.

### 6. Magic Numbers
In Python files, look for hardcoded numbers > 10 that aren't in constants files.

### 7. Potential Secrets
Search for patterns that look like hardcoded secrets:
- `AKIA` (AWS keys)
- `sk-` followed by long strings (OpenAI/Stripe)
- `ghp_` (GitHub tokens)
- Connection strings with passwords

Skip `.env.example` files.

### 8. DRY Violations
Look for obvious code duplication:
- Very similar functions
- Repeated string literals (same long string 3+ times)
- Copy-pasted code blocks

## Output Format

Provide a summary report like this:

```
## Vibe Check Report

### Summary
- X issues found across Y files
- Z high priority (secrets, hardcoded URLs)
- W low priority (TODOs, debug statements)

### High Priority (fix before committing)

#### Potential Secrets
- file.py:42 - Looks like an API key

#### Hardcoded URLs
- api.ts:15 - localhost URL should use env var

### Medium Priority (fix soon)

#### Empty Catch Blocks
- service.py:88 - except: pass (silently swallows errors)

#### snake_case in TypeScript
- types.ts:12 - `user_id` should be `userId`

### Low Priority (nice to fix)

#### Debug Statements
- utils.py:23 - print() statement
- component.tsx:45 - console.log()

#### TODO/FIXME
- auth.py:67 - TODO: implement refresh token

### Clean Areas
- No magic numbers found
- No DRY violations detected
```

If everything looks good:

```
## Vibe Check Report

✨ Looking good! No issues found.

Your code is clean and ready to ship.
```

## Notes

- Focus on **actionable** findings, not nitpicks
- Group by severity to help prioritize
- If a file has many issues, summarize rather than listing every line
- Be encouraging - the goal is to help, not shame
