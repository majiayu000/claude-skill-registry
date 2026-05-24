---
name: npm-publish
description: Guide for publishing packages to the npm registry. Use this skill when the user wants to publish a new package, release a new version, or manage npm package configurations.
---

# npm Publish Guide

This skill guides you through the process of publishing a package to the npm registry.

## 1. Prerequisites

Before publishing, ensure you are logged in to npm.

```bash
npm whoami
```

If not logged in:
```bash
npm login
```

## 2. Preparation & Configuration

### Critical `package.json` Fields
Ensure these fields are correct:
- **name**: Unique package name (scoped names like `@org/pkg` are recommended for organizations).
- **version**: SemVer compliant version (e.g., `1.0.0`).
- **main/module/exports**: Entry points for your library.
- **files**: Whitelist of files to include (reduces package size).
- **private**: Must be `false` (or missing) to publish.

### Excluding Files
Use a `.npmignore` file or the `files` array in `package.json` to prevent publishing unnecessary files (tests, src, config files).
**Tip**: `npm publish --dry-run` shows exactly what will be packed.

### Build (If applicable)
If your package requires compilation (TypeScript, Babel, etc.), run the build script first.
```bash
npm run build
```

## 3. Versioning

Update the package version before publishing. This command increments the version in `package.json` and creates a git tag.

```bash
# Choose one:
npm version patch # 1.0.0 -> 1.0.1
npm version minor # 1.0.0 -> 1.1.0
npm version major # 1.0.0 -> 2.0.0
```

## 4. Publishing

### Dry Run
Always do a dry run first to verify contents.
```bash
npm publish --dry-run
```

### Scoped Packages
If publishing a scoped package (e.g., `@myorg/my-pkg`) publicly for the first time:
```bash
npm publish --access public
```

### Standard Publish
```bash
npm publish
```

## 5. Post-Publish

### Push Tags
Push the new version commit and tags to your git repository.
```bash
git push --follow-tags
```

### Verification
Check the npm registry or install the package in a test project to verify.
```bash
npm view <package-name> version
```
