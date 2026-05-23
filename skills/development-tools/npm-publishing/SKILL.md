---
name: npm-publishing
# prettier-ignore
description: Use when publishing npm packages - covers package.json configuration, versioning, and provenance
---

# npm Publishing Best Practices

## Quick Start

```json
{
  "name": "lea-lang",
  "version": "1.0.0",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "files": ["dist"],
  "scripts": {
    "build": "tsc",
    "prepublishOnly": "npm run build && npm test"
  }
}
```

## Package Configuration

### Essential Fields

```json
{
  "name": "lea-lang",
  "version": "1.1.3",
  "description": "Pipe-oriented functional programming language",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "bin": {
    "lea": "./dist/cli/index.js"
  },
  "files": [
    "dist",
    "README.md"
  ],
  "keywords": ["language", "interpreter", "functional", "pipes"],
  "author": "Your Name",
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/user/lea.git"
  },
  "engines": {
    "node": ">=18"
  }
}
```

### Exports (Modern)

```json
{
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.js"
    },
    "./parser": {
      "types": "./dist/parser.d.ts",
      "import": "./dist/parser.mjs",
      "require": "./dist/parser.js"
    }
  }
}
```

## Versioning

### Semantic Versioning

```
MAJOR.MINOR.PATCH

1.0.0 → 1.0.1  # Patch: bug fixes
1.0.1 → 1.1.0  # Minor: new features (backwards compatible)
1.1.0 → 2.0.0  # Major: breaking changes
```

### Version Commands

```bash
npm version patch  # 1.0.0 → 1.0.1
npm version minor  # 1.0.0 → 1.1.0
npm version major  # 1.0.0 → 2.0.0
```

## Publishing

### First-Time Setup

```bash
npm login
npm publish --access public  # For scoped packages
```

### With Provenance (Recommended)

```bash
npm publish --provenance --access public
```

### Dry Run

```bash
npm publish --dry-run
npm pack  # Creates tarball to inspect
```

## Files to Include/Exclude

### .npmignore

```
src/
__tests__/
tests/
*.test.ts
.github/
docs/
```

### Or use package.json "files"

```json
{
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ]
}
```

## Pre-publish Checks

```json
{
  "scripts": {
    "prepublishOnly": "npm run build && npm test && npm run lint"
  }
}
```

## Reference Files

- [references/scopes.md](references/scopes.md) - Scoped packages
- [references/tags.md](references/tags.md) - Dist tags (latest, beta, next)
