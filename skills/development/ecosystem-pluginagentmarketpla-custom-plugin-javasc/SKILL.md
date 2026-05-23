---
name: ecosystem
description: JavaScript ecosystem including npm, build tools (Webpack, Vite), testing (Jest, Vitest), linting, and CI/CD integration.
sasmp_version: "1.3.0"
bonded_agent: 07-javascript-ecosystem
bond_type: PRIMARY_BOND

# Production-Grade Configuration
skill_type: reference
response_format: code_first
max_tokens: 1500

parameter_validation:
  required: [topic]
  optional: [tool_type]

retry_logic:
  on_ambiguity: ask_clarification
  fallback: show_npm_basics

observability:
  entry_log: "Ecosystem skill activated"
  exit_log: "Ecosystem reference provided"
---

# JavaScript Ecosystem Skill

## Quick Reference Card

### npm Commands
```bash
npm init -y                  # Initialize
npm install pkg              # Add dependency
npm install -D pkg           # Dev dependency
npm install -g pkg           # Global
npm update                   # Update all
npm audit fix                # Fix vulnerabilities
npm run script               # Run script
```

### package.json
```json
{
  "name": "project",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest",
    "lint": "eslint src"
  },
  "dependencies": {},
  "devDependencies": {}
}
```

### Vite Config (Recommended)
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: { port: 3000 },
  build: { sourcemap: true }
});
```

### Vitest Testing
```javascript
import { describe, it, expect, vi } from 'vitest';

describe('Calculator', () => {
  it('adds numbers', () => {
    expect(add(2, 3)).toBe(5);
  });

  it('mocks function', () => {
    const mock = vi.fn().mockReturnValue(42);
    expect(mock()).toBe(42);
  });
});
```

### ESLint Config
```javascript
// .eslintrc.cjs
module.exports = {
  env: { browser: true, es2022: true },
  extends: ['eslint:recommended'],
  rules: {
    'no-console': 'warn',
    'no-unused-vars': 'error'
  }
};
```

### Prettier Config
```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5"
}
```

### GitHub Actions CI
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm ci
      - run: npm test
      - run: npm run build
```

## Troubleshooting

### Common Issues

| Problem | Symptom | Fix |
|---------|---------|-----|
| Module not found | Import error | Check node_modules |
| Build fails | Compilation error | Check config |
| Test fails | Assertion error | Check test setup |
| Lint errors | Code warnings | Run `--fix` |

### Debug Checklist
```bash
# 1. Clear caches
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# 2. Check versions
node --version
npm --version
npm ls <package>

# 3. Verbose output
npm run build --verbose
```

## Production Patterns

### Environment Variables
```javascript
// .env
VITE_API_URL=https://api.example.com

// Usage
const url = import.meta.env.VITE_API_URL;
```

### Code Splitting
```javascript
// Dynamic import
const Component = React.lazy(() => import('./Component'));

// With Suspense
<Suspense fallback={<Loading />}>
  <Component />
</Suspense>
```

## Related

- **Agent 07**: JavaScript Ecosystem (detailed learning)
- **Skill: testing**: Test frameworks
- **Skill: modern-javascript**: ES modules
