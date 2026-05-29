---
name: latest-docs
description: |
  Fetch and verify latest official documentation before implementation. Use when implementing features with any library, framework, or technology. Prevents outdated patterns and deprecated API usage.
metadata:
  context: implementation, development, library, framework, api
  auto-trigger: true
---

# Latest Documentation Check

## Purpose

Ensure implementations follow the latest official documentation.
Prevent usage of deprecated APIs, outdated patterns, or breaking changes.

## When to Use

### Automatic Triggers
- Before implementing features using external libraries/frameworks
- Before using APIs that may have version-specific behavior
- When upgrading or migrating dependencies
- When user mentions specific library/framework versions

### Manual Check
- When uncertain about current best practices
- When documentation may have changed since knowledge cutoff

## Process

### Step 1: Identify Technologies

List all technologies/libraries involved in the implementation:
- Framework (React, Vue, Next.js, etc.)
- Libraries (axios, lodash, etc.)
- Runtime (Node.js, Deno, Bun, etc.)
- Language features (TypeScript, Go, Python version)

### Step 2: Fetch Latest Documentation

Use WebSearch to find current official documentation:

```
WebSearch: "[library name] official documentation [current year]"
WebSearch: "[library name] latest version changelog"
WebSearch: "[library name] migration guide"
```

### Step 3: Verify Version Compatibility

Check:
- Current stable version
- Breaking changes from previous versions
- Deprecated APIs to avoid
- New recommended patterns

### Step 4: Document References

In your implementation response, include:
- Documentation URL referenced
- Version number verified
- Any deprecation warnings noted

## Quick Reference

| Check | Search Query |
|-------|-------------|
| Latest version | `[lib] latest version [year]` |
| Best practices | `[lib] best practices [year]` |
| Deprecations | `[lib] deprecated api` |
| Migration | `[lib] migration guide v[X] to v[Y]` |

## Important Reminders

1. **Always verify version** - Project may use different version than latest
2. **Check package.json/go.mod** - Confirm actual version in use
3. **Note breaking changes** - Inform user of any migration needs
4. **Cite sources** - Include documentation URLs in response

## Output Format

When referencing documentation, include:

```
Documentation verified:
- [Library]: v[X.Y.Z] (https://...)
- Last checked: [date]
- Notes: [any deprecations or important changes]
```
