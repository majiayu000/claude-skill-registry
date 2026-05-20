---
name: parcel
description: Parcel zero-config bundler. Use for simple bundling.
---

# Parcel

Parcel is the "Zero Config" bundler. It works out of the box for React, Vue, Rust (Wasm), and more. v2.12 uses **Lightning CSS** for extreme performance.

## When to Use

- **Prototypes**: You just want `index.html` to work.
- **Simple Apps**: You don't want to maintain a 500-line config file.
- **Polyglot**: You have images, Rust, and SCSS mixed together.

## Core Concepts

### Zero Config

It auto-detects transforms. If you `import './style.scss'`, it installs `sass` automatically.

### Caching

Aggressive filesystem caching makes restarts instant.

### Workers

Parallelizes work across all cores.

## Best Practices (2025)

**Do**:

- **Use `<script type="module">`**: Point Parcel at your HTML file as the entry.
- **Use `macros`**: Parcel supports build-time macros.

**Don't**:

- **Don't fight the auto-install**: Let Parcel manage its plugins.

## References

- [Parcel Documentation](https://parceljs.org/)
