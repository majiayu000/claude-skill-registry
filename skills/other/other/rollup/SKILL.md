---
name: rollup
description: Rollup ES module bundler. Use for library bundling.
---

# Rollup

Rollup (v4) is the bundler of choice for **libraries**. It produces smaller, cleaner code than Webpack and pioneered Tree Shaking.

## When to Use

- **NPM Packages**: Building a library for others to use.
- **Flat Bundling**: "Scope Hoisting" puts everything in one closure for performance.

## Core Concepts

### Tree Shaking

Rollup analyzes the import graph and excludes unused code statically.

### Formats

Outputs `esm`, `cjs`, `umd`, `iife`.

### Plugins

The ecosystem that Vite adopted.

## Best Practices (2025)

**Do**:

- **Use `pkg.exports`**: Configure `package.json` exports correctly for ESM/CJS dual publish.
- **Externalize dependencies**: Don't bundle `react` into your library. Mark it as external.

**Don't**:

- **Don't use for Apps**: Use Vite (which uses Rollup internally) for apps. Use Rollup directly for libs.

## References

- [Rollup Documentation](https://rollupjs.org/)
