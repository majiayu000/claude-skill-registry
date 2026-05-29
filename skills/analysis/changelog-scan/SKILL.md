---
name: changelog-scan
description: Scan Claude Code changelog for new versions, features, and changes. Fetches official docs, parses release notes, and generates structured update report.
argument-hint: "[--since <version>]"
user-invocable: true
---

# Changelog Scan Skill

## Overview

Fetches and analyzes the official Claude Code changelog to detect new versions and changes.

## Data Sources

| Source | URL | Method |
|--------|-----|--------|
| Changelog | code.claude.com/docs/en/changelog.md | WebFetch |
| Docs Index | code.claude.com/docs/llms.txt | WebFetch |
| Hooks Ref | code.claude.com/docs/en/hooks.md | WebFetch |
| Plugins Ref | code.claude.com/docs/en/plugins-reference.md | WebFetch |
| CLI Ref | code.claude.com/docs/en/cli-reference.md | WebFetch |

## Workflow

1. **Fetch** changelog via WebFetch or scripts/fetch-changelog.sh
2. **Parse** version numbers and release dates
3. **Extract** changes per version (features, fixes, breaking)
4. **Compare** with last known version from state file
5. **Generate** report using templates/changelog-report.md

## Version Detection

Parse patterns from changelog:
- `## vX.Y.Z` or `## X.Y.Z` - Version headers
- `### Breaking Changes` - Breaking section
- `### New Features` - Features section
- `### Bug Fixes` - Fixes section

## State File

Location: `~/.claude/logs/00-changelog/{date}-state.json`

## References

- [Sources Reference](references/sources.md)
- [Report Template](references/templates/changelog-report.md)
