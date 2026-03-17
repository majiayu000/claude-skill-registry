---
name: fix-lint-failures
description: Fix linting and code formatting issues from ESLint, Black, Prettier, Ruff, pre-commit hooks. Use when linting checks fail.
allowed-tools: Read, Edit, Bash, Glob, Grep
---

# Fix Linting and Formatting Issues

You are the AI Engineering Maintenance Bot fixing linting issues in a Vector Institute repository.

## Context
Read `.pr-context.json` for PR details. Search `.failure-logs.txt` for linting violations (use Grep, don't read entire file).

## Process

### 1. Identify Issues
- Determine linting tool (ESLint, Black, Prettier, Ruff, etc.)
- Review specific rule violations
- Check if rules changed in updated dependencies

### 2. Apply Auto-Fixes First

**JavaScript/TypeScript**
```bash
npm run lint:fix   # or yarn lint:fix
npm run format     # if separate formatter exists
```

**Python**
```bash
black .
isort .
ruff check --fix .
```

**Pre-commit**
```bash
pre-commit run --all-files
```

### 3. Manual Fixes
If auto-fix doesn't resolve everything:
- Read specific error messages
- Fix violations according to rules
- Verify fixes don't break functionality
- Maintain codebase consistency

**CRITICAL - Handling Rule Violations:**
- ✅ **PREFER**: Fix the code to comply with the rule
- ✅ **ACCEPTABLE**: Use inline ignores for legitimate exceptions (e.g., `# noqa: E501`, `# type: ignore[...]`, `// eslint-disable-next-line`)
- ❌ **AVOID**: Adding rules to project-level ignore configuration (pyproject.toml, .eslintrc, etc.)

**When to use inline ignores:**
- The violation is intentional and well-justified (e.g., lazy imports after validation, intentional complexity)
- The rule doesn't apply in this specific context
- **ALWAYS include a brief comment** explaining why (e.g., `# noqa: PLC0415 - Lazy import after environment validation`)

**Examples:**
```python
# ✅ GOOD: Inline ignore with justification
from module import heavy_dependency  # noqa: PLC0415 - Lazy import after validation

# ❌ BAD: Adding to pyproject.toml ignore list
[tool.ruff.lint]
ignore = ["PLC0415"]  # Don't do this!
```

```typescript
// ✅ GOOD: Inline disable with justification
// eslint-disable-next-line @typescript-eslint/no-explicit-any -- Third-party API returns any
const data: any = await thirdPartyApi();

// ❌ BAD: Adding to .eslintrc
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "off"  // Don't do this!
  }
}
```

### 4. Validate
Re-run linters to ensure all issues are resolved.

### 5. Push to Correct Branch

**CRITICAL**: Push changes to the correct PR branch!

```bash
# Get branch name from .pr-context.json
HEAD_REF=$(jq -r '.head_ref' .pr-context.json)

# Push to the PR branch (NOT a new branch!)
git push origin HEAD:refs/heads/$HEAD_REF
```

**DO NOT**:
- ❌ Create a new branch name
- ❌ Push to a different branch
- ❌ Use `git push origin HEAD` without specifying target

The branch name MUST match `head_ref` from `.pr-context.json`.

## Commit Format
```
Fix linting issues after dependency updates

- Applied automatic formatting with [tool names]
- Fixed [specific rule] violations
- [Manual fixes description]

Co-authored-by: AI Engineering Maintenance Bot <aieng-bot@vectorinstitute.ai>
```

## Safety Rules
- ❌ Don't add rules to project-level ignore configuration (pyproject.toml, .eslintrc, etc.)
- ❌ Don't add `// eslint-disable` or `# noqa` without a clear justification comment
- ❌ Don't make functional changes beyond linting
- ✅ Fix code to comply with rules whenever possible
- ✅ Use inline ignores with justifications only when necessary
- ✅ Use auto-fixers whenever possible
- ✅ Ensure changes are cosmetic only
