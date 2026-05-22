---
name: coding-standards-enforcer
description: Automated code style enforcement with linters, formatters, and pre-commit hooks for consistent codebases
license: MIT
metadata:
  adapted-by: ai-skills
  category: code-quality
---

# Coding Standards Enforcer

Automate code quality and consistency with linters, formatters, and hooks.

## ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier'
  ],
  rules: {
    'no-console': 'warn',
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    'react/prop-types': 'off',
    'complexity': ['warn', 10],
    'max-lines-per-function': ['warn', 50]
  }
};
```

## Prettier Configuration

```json
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "avoid"
}
```

## Pre-commit Hooks

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{json,md}": [
      "prettier --write"
    ]
  }
}
```

## Git Hooks Setup

```bash
# Install husky
npm install --save-dev husky lint-staged

# Initialize husky
npx husky install

# Add pre-commit hook
npx husky add .husky/pre-commit "npx lint-staged"
```

## Naming Conventions

```typescript
// PascalCase for classes and types
class UserService {}
type UserData = {};

// camelCase for functions and variables
function getUserById() {}
const userName = 'John';

// UPPER_SNAKE_CASE for constants
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';

// kebab-case for files
// user-service.ts
// api-client.ts
```

## Integration Points

Complements:
- **verification-loop**: For pre-commit validation
- **tdd-workflow**: For test standards
- **code-refactoring-patterns**: For style improvement
