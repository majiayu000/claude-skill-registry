---
name: npm
description: npm Node.js package manager and registry. Use for JavaScript dependencies.
---

# npm

npm is the default package manager for Node.js. v11 (2025) introduces strict publishing rules and `npx` caching improvements.

## When to Use

- **Default**: It comes with Node. Zero friction.
- **Compatibility**: The standard `package-lock.json` is supported everywhere.
- **Publishing**: `npm publish` is the canonical way to share JS code.

## Quick Start

```bash
npm init -y
npm install lodash
npm install --save-dev jest

# Monorepo
npm init -w packages/my-lib
```

## Core Concepts

### package.json

Manifest file. Scripts, dependencies, metadata.

### package-lock.json

Locks dependency tree for reproducible builds. **Commit this**.

### Workspaces

Native monorepo support.
`npm install` installs dependencies for root and all nested packages.

## Best Practices (2025)

**Do**:

- **Use `npm ci`**: For CI/CD pipelines. Faster and strict (fails if lockfile doesn't match).
- **Audit**: `npm audit` to find vulnerabilities.
- **Use Scopes**: `@my-org/my-pkg` to avoid name collisions.

**Don't**:

- **Don't mix managers**: Don't use `yarn` in a repo with `package-lock.json`.

## References

- [npm Documentation](https://docs.npmjs.com/)
