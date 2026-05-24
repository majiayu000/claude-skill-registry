---
name: prettier
description: Code formatting with Prettier for consistent style across the codebase. Auto-formatting, configuration, editor integration. Trigger: When configuring Prettier formatting, setting up auto-format, or ensuring consistent code style.
skills:
  - conventions
dependencies:
  prettier: ">=3.0.0 <4.0.0"
allowed-tools:
  - documentation-reader
  - web-search
---

# Prettier Skill

## Overview

Automatic code formatting with Prettier for consistent code style.

## Objective

Configure and use Prettier to maintain consistent formatting across JavaScript, TypeScript, CSS, and other supported files.

---

## When to Use

Use this skill when:

- Setting up automatic code formatting
- Configuring format-on-save in editors
- Ensuring consistent code style across team
- Integrating formatting into CI/CD
- Formatting multiple file types (JS, TS, CSS, JSON, Markdown)

Don't use this skill for:

- Linting logic/quality rules (use eslint skill)
- TypeScript type checking (use typescript skill)

---

## Critical Patterns

### ✅ REQUIRED: Use Project Config File

```json
// ✅ CORRECT: .prettierrc in project root
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 80
}

// ❌ WRONG: Relying on editor defaults (inconsistent)
// No config file
```

### ✅ REQUIRED: Format on Save

```json
// ✅ CORRECT: VS Code settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode"
}
```

### ✅ REQUIRED: Integrate with ESLint

```javascript
// ✅ CORRECT: Disable ESLint formatting rules
module.exports = {
  extends: ["eslint:recommended", "prettier"], // Must be last
};
```

---

## Conventions

- Use project .prettierrc configuration
- Format on save recommended
- Integrate with ESLint

### Prettier Specific

- Configure print width (default 80)
- Set semicolons preference
- Configure quote style
- Set trailing commas
- Configure tab width

---

## Decision Tree

**Team prefers no semicolons?** → Set `"semi": false`.

**Using single quotes?** → Set `"singleQuote": true`.

**Long lines?** → Adjust `"printWidth"` (default 80, consider 100-120).

**Tabs vs spaces?** → Set `"useTabs"` and `"tabWidth"`.

**Trailing commas?** → Set `"trailingComma": "es5"` (compatible) or `"all"` (modern).

**Ignore files?** → Create `.prettierignore` file.

**Format specific files?** → Run `prettier --write "src/**/*.{js,ts,tsx}"`.

---

## Example

`.prettierrc`:

```json
{
  "semi": true,
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

---

## Edge Cases

**Prettier vs ESLint conflicts:** Use `eslint-config-prettier` to disable conflicting ESLint rules.

**Ignored files:** Add patterns to `.prettierignore` (similar to `.gitignore`).

**Overriding for specific files:** Use `overrides` in config for per-file-pattern settings.

**Pre-commit formatting:** Use husky + lint-staged to format only staged files.

**Editor integration:** Ensure Prettier extension is installed and set as default formatter.

---

## References

- https://prettier.io/docs/en/
- https://prettier.io/docs/en/configuration.html
