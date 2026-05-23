---
name: eslint
description: "Enforcing code quality and best practices using ESLint in JavaScript and TypeScript projects. Configuration, rules, plugins, auto-fix. Trigger: When configuring ESLint rules, fixing linting errors, or enforcing code quality standards."
skills:
  - conventions
  - typescript
  - javascript
dependencies:
  eslint: ">=8.0.0 <9.0.0"
allowed-tools:
  - documentation-reader
  - web-search
  - file-reader
---

# ESLint Skill

## Overview

This skill provides guidance for configuring and using ESLint to enforce code quality, consistency, and best practices in JavaScript and TypeScript projects.

## Objective

Enable developers to maintain code quality through automated linting with proper ESLint configuration, rules, and integration with development workflow.

---

## When to Use

Use this skill when:

- Configuring ESLint for JavaScript/TypeScript projects
- Setting up linting rules and plugins
- Fixing linting errors in code
- Integrating ESLint with editors and CI/CD
- Enforcing code quality standards

Don't use this skill for:

- Code formatting only (use prettier skill)
- TypeScript type checking (use typescript skill)
- Build configuration (use vite or webpack skills)

---

## Critical Patterns

### ✅ REQUIRED: Extend Recommended Configs

```javascript
// ✅ CORRECT: Extend recommended configs
module.exports = {
  extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
};

// ❌ WRONG: Starting from scratch
module.exports = {
  rules: {
    /* manually defining everything */
  },
};
```

### ✅ REQUIRED: Use TypeScript Parser for TS Projects

```javascript
// ✅ CORRECT: TypeScript parser
module.exports = {
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint"],
};

// ❌ WRONG: Default parser for TypeScript
module.exports = {
  // No parser specified for .ts files
};
```

### ✅ REQUIRED: Run in CI/CD

```json
// package.json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix"
  }
}
```

---

## Conventions

- Use ESLint with TypeScript parser for TypeScript projects
- Extend recommended configurations
- Customize rules to match project standards
- Integrate with editor for real-time feedback
- Run ESLint in CI/CD pipeline

---

## Decision Tree

**TypeScript project?** → Use `@typescript-eslint/parser` and `@typescript-eslint/recommended`.

**React project?** → Add `plugin:react/recommended` and `plugin:react-hooks/recommended`.

**Need auto-fix?** → Run `eslint --fix`, configure editor to fix on save.

**Custom rule needed?** → Add to `rules` object with "error", "warn", or "off".

**Disable rule for line?** → Use `// eslint-disable-next-line rule-name`.

**Monorepo?** → Use multiple `.eslintrc` files or override patterns.

**Conflicting with Prettier?** → Use `eslint-config-prettier` to disable formatting rules.

---

## Example

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended",
  ],
  parser: "@typescript-eslint/parser",
  plugins: ["@typescript-eslint", "react", "react-hooks"],
  rules: {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "react/prop-types": "off",
  },
};
```

## Edge Cases

- Handle monorepo configurations
- Configure for multiple environments (node, browser)
- Manage rule exceptions with inline comments
- Balance strictness with developer experience

## References

- https://eslint.org/docs/latest/
- https://typescript-eslint.io/
