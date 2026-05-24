---
name: eslint
description: ESLint JavaScript linter with plugins. Use for code quality.
---

# ESLint

ESLint is the standard linter for JS/TS. v9 (2024/2025) moved to **Flat Config** (`eslint.config.js`), a major breaking change that simplifies configuration.

## When to Use

- **Enforcing Rules**: `no-unused-vars`, `react-hooks/rules-of-hooks`.
- **Code Quality**: Catching bugs before they run.

## Core Concepts

### Flat Config (`eslint.config.js`)

An array of objects. No more `extends` string hell.

```js
export default [js.configs.recommended, { rules: { semi: "error" } }];
```

### Plugins

NPM packages that add rules. `eslint-plugin-react`.

### Parsers

`@typescript-eslint/parser` allows ESLint to understand TS.

## Best Practices (2025)

**Do**:

- **Use Flat Config**: Use the new format.
- **Use `typescript-eslint`**: The typed linting rules are powerful (e.g. `no-floating-promises`).

**Don't**:

- **Don't configure formatting rules**: Disable all formatting rules (use Prettier or Biome for that). use `eslint-config-prettier`.

## References

- [ESLint Documentation](https://eslint.org/)
