---
name: standards-enforcement
description: Establish and enforce coding standards, best practices, and architectural patterns across the codebase using linters, formatters, and code review processes. Use when setting up ESLint/Prettier, configuring linting rules, creating code style guides, implementing pre-commit hooks, establishing naming conventions, enforcing TypeScript strict mode, maintaining consistency, conducting architecture reviews, or defining team coding standards.
---

# Standards Enforcement - Maintaining Code Quality

## When to use this skill

- Setting up ESLint, Prettier, and code formatters
- Configuring linting rules and code standards
- Creating team code style guides
- Implementing pre-commit hooks with Husky
- Establishing naming conventions
- Enforcing TypeScript strict mode
- Maintaining code consistency across team
- Conducting code review for standards compliance
- Defining architectural patterns and rules
- Setting up import ordering and organization
- Enforcing test coverage requirements
- Creating and maintaining coding guidelines

## When to use this skill

- Setting up project guidelines, code reviews, enforcing best practices, maintaining consistency.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Setting up project guidelines, code reviews, enforcing best practices, maintaining consistency.

## Tools

### ESLint
```json
{
  "extends": ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
  "rules": {
    "no-console": "warn",
    "no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### Prettier
```json
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### Husky + lint-staged
```json
{
  "lint-staged": {
    "*.{js,ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md}": ["prettier --write"]
  }
}
```

## Resources
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)
- [Husky](https://typicode.github.io/husky/)
