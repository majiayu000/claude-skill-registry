---
description: Generate user-friendly changelog
allowed-tools: Bash Read Grep Glob
---

# Changelog Generation

## Run

```bash
git tag -l "v*" --sort=-version:refname | head -1
git log $(git tag -l "v*" --sort=-version:refname | head -1)..HEAD --oneline --no-merges
```

## Categorize

**Include:** feat, fix, perf, content changes, config improvements
**Exclude:** refactor, chore, test, docs, ci, build

## Rewrite for Users

Transform technical messages to plain language:

- Before: `fix(config): correct upload size limit`
- After: `Fixed file upload size limit`

- Before: `feat(content): add Poi techniques article`
- After: `Added article on poi spinning techniques`

- Before: `fix(caddy): security headers for uploads`
- After: `Improved security for file uploads`

## Output Format

```
### Bug Fixes
- [plain language]

### New Features
- [plain language]

### Improvements
- [plain language]
```
