---
name: shared-changelog
description: Generate CHANGELOG.md from conventional commits with semantic versioning.
argument-hint: "[--version <v>] [--from <tag>] [--dry-run]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Generate or update CHANGELOG.md from Git history using conventional commits. Supports semantic versioning and release automation.

## Arguments
- `--version <v>` — Target version (e.g., `1.2.0`). If omitted, suggests based on commit types.
- `--from <tag>` — Starting point (default: last tag or initial commit)
- `--dry-run` — Show changelog without writing

## Version inference
Based on commits since last tag:
- `feat` with `BREAKING CHANGE` → **major** bump
- `feat` → **minor** bump
- `fix`, `perf` → **patch** bump

## Commit categories
| Type | Changelog section |
|------|------------------|
| `feat` | ✨ Features |
| `fix` | 🐛 Bug Fixes |
| `perf` | ⚡ Performance |
| `docs` | 📚 Documentation |
| `refactor` | ♻️ Refactoring |
| `test` | 🧪 Tests |
| `build`, `ci` | 🔧 Build & CI |
| `chore` | Hidden (unless --all) |

## Changelog format
```markdown
# Changelog

## [1.2.0] - 2025-01-24

### ✨ Features
- **auth:** add biometric login (#42)

### 🐛 Bug Fixes
- **api:** handle network timeout (#38)

### ⚠️ Breaking Changes
- **config:** rename ENV_VAR to NEW_NAME
```

## Workflow
1. Parse commits since last tag
2. Group by type and scope
3. Infer version (or use provided)
4. Generate changelog entry
5. Prepend to CHANGELOG.md (or create)
6. Optionally create git tag

## Output
- Suggested version
- Changelog preview
- File updated (unless --dry-run)

## Reference
For templates and customization, see `reference/shared-changelog-reference.md`
