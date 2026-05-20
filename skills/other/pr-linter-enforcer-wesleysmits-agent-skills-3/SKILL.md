---
name: enforcing-code-linting
description: Runs ESLint, Prettier, and stylelint against changed files and suggests or applies fixes. Use when the user mentions linting, code style, PR review, formatting issues, or wants to check code quality before committing.
---

# PR Reviewer / Linter Enforcer

## When to use this skill

- User asks to lint or format code
- User wants to review code quality before a PR
- User mentions ESLint, Prettier, or stylelint
- User asks to fix formatting or style issues
- User wants to check changed files for violations
- User mentions code consistency or style enforcement

## Workflow

- [ ] Identify changed files (staged or branch diff)
- [ ] Detect available linting tools in project
- [ ] Run linters against changed files only
- [ ] Collect and categorize issues
- [ ] Present issues with fix suggestions
- [ ] Apply automatic fixes if requested
- [ ] Verify fixes resolved issues

## Instructions

### Step 1: Identify Changed Files

For staged changes:

```bash
git diff --cached --name-only --diff-filter=ACMR
```

For branch comparison:

```bash
git diff --name-only origin/main...HEAD
```

Filter to lintable files:

```bash
git diff --cached --name-only --diff-filter=ACMR | grep -E '\.(js|jsx|ts|tsx|vue|css|scss|json|md)$'
```

### Step 2: Detect Available Linters

Check for linter configurations in project root:

| Tool      | Config Files                                           |
| --------- | ------------------------------------------------------ |
| ESLint    | `.eslintrc.*`, `eslint.config.*`, `package.json`       |
| Prettier  | `.prettierrc.*`, `prettier.config.*`, `package.json`   |
| stylelint | `.stylelintrc.*`, `stylelint.config.*`, `package.json` |

Verify tools are installed:

```bash
npm ls eslint prettier stylelint 2>/dev/null || yarn list --pattern "eslint|prettier|stylelint" 2>/dev/null
```

### Step 3: Run Linters on Changed Files

**ESLint** (JavaScript/TypeScript):

```bash
npx eslint --format stylish <files>
```

With auto-fix preview:

```bash
npx eslint --fix-dry-run --format json <files>
```

**Prettier** (formatting):

```bash
npx prettier --check <files>
```

Show what would change:

```bash
npx prettier --write --list-different <files>
```

**stylelint** (CSS/SCSS):

```bash
npx stylelint <css-files>
```

### Step 4: Categorize Issues

Group issues by severity and type:

**Errors** (must fix):

- Syntax errors
- Type errors
- Security vulnerabilities
- Unused variables in critical paths

**Warnings** (should fix):

- Unused imports
- Missing accessibility attributes
- Deprecated API usage

**Style** (nice to fix):

- Formatting inconsistencies
- Naming conventions
- Import ordering

### Step 5: Present Issues

Format findings clearly:

```markdown
## Linting Report

### Errors (3)

| File         | Line | Rule                               | Message                              |
| ------------ | ---- | ---------------------------------- | ------------------------------------ |
| src/utils.ts | 42   | @typescript-eslint/no-explicit-any | Unexpected any                       |
| src/api.ts   | 15   | no-unused-vars                     | 'response' is defined but never used |
| src/index.ts | 8    | import/no-unresolved               | Unable to resolve path               |

### Warnings (2)

| File           | Line | Rule                                     | Message                   |
| -------------- | ---- | ---------------------------------------- | ------------------------- |
| src/Button.tsx | 23   | jsx-a11y/click-events-have-key-events    | Missing keyboard handler  |
| src/utils.ts   | 67   | @typescript-eslint/no-non-null-assertion | Avoid non-null assertions |

### Formatting (5 files)

- src/components/Card.tsx
- src/hooks/useAuth.ts
- src/pages/Home.tsx
- src/styles/main.css
- src/types/index.ts
```

### Step 6: Apply Fixes

**Auto-fix all fixable issues:**

```bash
npx eslint --fix <files>
npx prettier --write <files>
npx stylelint --fix <css-files>
```

**Fix specific rule categories:**

```bash
# Only formatting fixes
npx eslint --fix --rule 'indent: error' --rule 'semi: error' <files>

# Only import sorting
npx eslint --fix --rule 'import/order: error' <files>
```

### Step 7: Verify Fixes

Re-run linters to confirm resolution:

```bash
npx eslint <files> && npx prettier --check <files> && echo "✓ All checks passed"
```

## Configuration Detection

### ESLint Config Patterns

Check for flat config (ESLint 9+):

```bash
ls eslint.config.{js,mjs,cjs} 2>/dev/null
```

Check for legacy config:

```bash
ls .eslintrc.{js,cjs,json,yml,yaml} 2>/dev/null
```

### Prettier Config Patterns

```bash
ls .prettierrc{,.json,.yml,.yaml,.js,.cjs,.mjs} prettier.config.{js,cjs,mjs} 2>/dev/null
```

### Package.json Scripts

Check for existing lint scripts:

```bash
npm pkg get scripts.lint scripts.format scripts.style 2>/dev/null
```

Prefer using project scripts when available:

```bash
npm run lint -- --fix
npm run format
```

## Common Fix Patterns

### Unused Imports

```typescript
// Before
import { useState, useEffect, useCallback } from "react";
// Only useState used

// After
import { useState } from "react";
```

### Missing Accessibility

```tsx
// Before
<div onClick={handleClick}>Click me</div>

// After
<button type="button" onClick={handleClick}>Click me</button>
```

### Formatting Issues

```typescript
// Before
const obj = { foo: "bar", baz: 42 };

// After
const obj = { foo: "bar", baz: 42 };
```

## Integration with Git Hooks

If user wants pre-commit enforcement, suggest:

```bash
npx husky add .husky/pre-commit "npx lint-staged"
```

With `lint-staged` config in `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{css,scss}": ["stylelint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

## Validation

Before completing:

- [ ] All errors are resolved or acknowledged
- [ ] Warnings reviewed and addressed where appropriate
- [ ] Formatting is consistent
- [ ] No new issues introduced by fixes
- [ ] Changes staged for commit

## Error Handling

- **Linter not installed**: Run `npm install --save-dev <tool>` or check if project uses yarn/pnpm.
- **No config found**: Linter may use defaults. Run `npx <tool> --init` to create config.
- **Command fails**: Run `npx <tool> --help` for available options.
- **No changed files**: Run `git status` to verify. May need to stage changes first.

## Resources

- [ESLint Documentation](https://eslint.org/docs/latest/)
- [Prettier Documentation](https://prettier.io/docs/en/)
- [stylelint Documentation](https://stylelint.io/)
- [lint-staged](https://github.com/okonet/lint-staged)
