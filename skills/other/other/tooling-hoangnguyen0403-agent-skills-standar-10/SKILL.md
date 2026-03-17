---
name: JavaScript Tooling
description: Development tools, linting, and testing for JavaScript projects.
metadata:
  labels: [tooling, javascript, eslint, prettier, testing]
  triggers:
    files: ['.eslintrc.*', 'jest.config.*', 'package.json']
    keywords: [eslint, prettier, jest, test, lint, build]
---

# JavaScript Tooling

## **Priority: P1 (OPERATIONAL)**

Essential tooling for JavaScript development.

## Implementation Guidelines

- **Linting**: ESLint (Rec + Prettier). Fix on save.
- **Formatting**: Prettier. Run on save/commit.
- **Testing**: Jest/Vitest. Co-locate tests. >80% cov.
- **Build**: Vite (Apps), Rollup (Libs).
- **Pkg Manager**: Sync versions (`npm`/`yarn`/`pnpm`).

## Anti-Patterns

- **No Formatting Wars**: Prettier rules.
- **No Untested Code**: TDD/Post-code tests.
- **No Dirty Commits**: Lint before push.

## Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: ['eslint:recommended', 'prettier'],
  rules: { 'no-console': 'warn', 'prefer-const': 'error' },
};
```

```json
// .prettierrc
{ "semi": true, "singleQuote": true, "printWidth": 80 }
```

```javascript
// jest.config.js
export default {
  coverageThreshold: { global: { lines: 80 } },
};
```

## Reference & Examples

For testing patterns and CI/CD:
See [references/REFERENCE.md](references/REFERENCE.md).

## Related Topics

best-practices | language
