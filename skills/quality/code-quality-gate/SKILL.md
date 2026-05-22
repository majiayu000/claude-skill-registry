---
name: code-quality-gate
description: Enforces automated quality checks before every deploy. Prevents production failures through a 5-stage Quality Gate System (Pre-Commit, PR-Check, Preview, E2E, Production). Activate on code changes, deployments, PR reviews, build failures.
---

# Code Quality Gate

This skill prevents production failures through a 5-stage Quality Gate System.

## The 5 Quality Gates

1. **Pre-Commit (local):** TypeScript, Lint, Format - blocks commit on errors
2. **PR-Check (GitHub Actions):** Unit Tests, Build - blocks merge on errors
3. **Preview Deploy:** Vercel/Netlify Preview URL for visual review
4. **E2E Tests:** Playwright against Preview, Lighthouse performance audit
5. **Production Deploy:** Only when ALL gates pass

## Critical Rules

- **CRITICAL:** NEVER use `continue-on-error: true` for TypeScript checks in GitHub Actions!
- Husky Setup: `npm install -D husky lint-staged && npx husky init`
- Rollback: `vercel rollback`

## Example: Pre-Commit Hook (.husky/pre-commit)

```bash
#!/bin/sh
npx lint-staged
npx tsc --noEmit
```

## Example: lint-staged.config.js

```javascript
module.exports = {
  '*.{ts,tsx}': ['eslint --fix', 'prettier --write'],
  '*.{json,md}': ['prettier --write'],
};
```

## Example: GitHub Actions Workflow

```yaml
name: Quality Gate
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      # Gate 1: TypeScript (NEVER skip!)
      - name: TypeScript Check
        run: npx tsc --noEmit

      # Gate 2: Linting
      - name: ESLint
        run: npm run lint

      # Gate 3: Unit Tests
      - name: Unit Tests
        run: npm run test

      # Gate 4: Build
      - name: Build
        run: npm run build
```

## When to Activate

- Code changes that touch production code
- Deployment requests
- PR reviews
- Build failures (for debugging)

## Real-World Impact

At [fabrikIQ.com](https://app.fabrikiq.com), this quality gate system caught:
- 2 TypeScript errors that would have caused runtime crashes
- 1 missing environment variable in the deploy
- 3 performance regressions before they hit production
