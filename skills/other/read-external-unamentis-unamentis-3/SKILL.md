---
name: read-external
description: Read-only access to external repositories for cross-repo context. Use when you need to reference code, patterns, or documentation from other local repositories.
allowed-tools: Read, Grep, Glob, Task
---

# Cross-Repository Read Access

This skill provides constrained read-only access to external repositories configured in `additionalDirectories`.

## Available External Repos

External repositories are configured in `.claude/settings.json` under `additionalDirectories`. Check that file for the current list of available repos and their absolute paths.

| Repo | Purpose |
|------|---------|
| *unamentis-android* | Android Client for UnaMentis |

## Usage

Access is always active via `additionalDirectories` in settings.json. When you need external context, use the absolute path from the settings:

1. **Find files**: Use `Glob` with the repo's absolute path (e.g., `{repo_path}/**/*.kt`)
2. **Search content**: Use `Grep` with pattern in the repo's absolute path
3. **Read files**: Use `Read` with absolute path from settings

Check `.claude/settings.json` for the exact paths configured on this machine.

## Constraints

When this skill is explicitly invoked with `/read-external`:
- ONLY Read, Grep, Glob, and Task tools are available
- No modifications to external repos (Edit/Write blocked)
- Reference and adapt code, don't copy wholesale

## Adding New Repositories

See [TEMPLATE.md](TEMPLATE.md) for step-by-step instructions on adding new external repositories.
