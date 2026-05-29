---
name: exploring-packages
description: Explore npm package source code locally. Use when needing to understand a library's API, types, or implementation.
---

# Exploring Packages

## Goal

Get npm package source code locally for reading, stored globally to amortize across projects.

## Location

All packages stored in: `~/.claude/package-sources/<package-name>/`

## Steps

### 1. Check if already exists

```bash
ls ~/.claude/package-sources/<package-name>/ 2>/dev/null
```

If exists, check if update needed:

```bash
cd ~/.claude/package-sources/<package-name> && npm outdated 2>/dev/null
```

### 2. Get package (prefer npm pack over git clone)

__CRITICAL__: Use `npm pack` + extract, NOT git clone. This gets the actual published package (post-build) matching what's installed in projects, not raw source that may need complex builds.

```bash
mkdir -p ~/.claude/package-sources/<package-name>
cd ~/.claude/package-sources/<package-name>
npm pack <package-name> && tar -xzf *.tgz --strip-components=1 && rm *.tgz
```

This gives you:

* Built/transpiled code (what projects actually import)
* Published types (.d.ts files)
* package.json with exports map

### 3. For source code (when published package isn't enough)

Only if you need original TypeScript source or tests:

```bash
# Get repo URL from package.json
npm view <package-name> repository.url

# Clone to separate directory
git clone --depth 1 <repo-url> ~/.claude/package-sources/<package-name>-src
```

### 4. Read the code

Start with:

* `package.json` - exports map, main entry
* Type definitions (.d.ts files)
* Actual implementation files

Use Serena MCP's symbolic tools for efficient navigation.

## Update existing package

```bash
cd ~/.claude/package-sources/<package-name>
rm -rf * && npm pack <package-name> && tar -xzf *.tgz --strip-components=1 && rm *.tgz
```

## Version-specific package

For specific version matching your project:

```bash
npm pack <package-name>@<version>
```

Check project's version:

```bash
cat package.json | grep '"<package-name>"'
# or
pnpm list <package-name>
```

## Notes

* Prefer `npm pack` over git clone - gets published output, not complex source
* Global location (~/.claude/package-sources/) amortizes across all projects
* Check existing before fetching - avoid re-downloading
* Match project version when debugging specific issues
