---
name: babel
description: Babel JavaScript compiler for compatibility. Use for transpiling.
---

# Babel

Babel is the transpiler that made ES6+ possible. While slower than SWC/esbuild, it remains the most **extensible** compiler with the largest plugin ecosystem.

## When to Use

- **Custom Transformations**: You need to write a custom AST transform for your framework.
- **Legacy Browser Support**: `preset-env` with `core-js` is still the gold standard for "make it run on IE11" (if you must).

## Core Concepts

### Presets

`@babel/preset-env`, `@babel/preset-react`, `@babel/preset-typescript`.

### Plugins

Small transforms. `plugin-transform-runtime`.

### Polyfills

Injecting missing features (Map, Set, Promise).

## Best Practices (2025)

**Do**:

- **Use SWC if possible**: Babel is slow.
- **Use `babel.config.json`**: Project-wide configuration.

**Don't**:

- **Don't transpile `node_modules`**: Unless absolutely necessary. It murders build time.

## References

- [Babel Documentation](https://babeljs.io/)
