---
name: sc-diff
version: 0.8.0
description: >
  Semantic diffing for .NET source using roslyn-diff. Supports file/folder diffs,
  HTML reports, and git/PR-aware comparisons (GitHub + Azure DevOps).
---

# sc-diff

## Capabilities
- Compare two files or two folders (exactly one of each per request)
- Auto semantic diff for .cs/.vb with line fallback for non-.NET files
- JSON-first output for AI consumption
- Optional HTML report per pair
- Git/PR-based comparisons via sc-git-diff
- Smart batching for large diff sets

## Agent Delegation
| Operation | Agent | Returns |
|-----------|-------|---------|
| File/folder diff | `sc-diff` | JSON: results[], counts, warnings |
| Git/PR diff | `sc-git-diff` | JSON: results[], refs, counts |

Invoke agents via Agent Runner using `.claude/agents/registry.yaml`.

## Parameters
- `files`: string (comma-delimited list of 2 file paths)
- `folders`: string (comma-delimited list of 2 folder paths)
- `html`: boolean (default false)
- `mode`: `auto` (default), `roslyn`, `line`
- `ignore_whitespace`: boolean (default false)
- `context_lines`: number (optional, default 3)
- `text_output`: string|bool (optional; true writes `.sc/roslyn-diff/temp/diff-#.txt`)
- `git_output`: string|bool (optional; true writes `.sc/roslyn-diff/temp/diff-#.patch`)
- `allow_large`: boolean (default false)
- `files_per_agent`: number (default 10)
- `max_pairs`: number (default 100)
- `git_pr`: string (PR URL or PR number)

## Behavior
1) Validate exactly one of `files` or `folders`.
2) Resolve inputs into file pairs.
3) If pair count > `max_pairs` and `allow_large` is false, stop with a warning.
4) If pair count > `files_per_agent`, split into batches and spawn sub-agents.
5) Aggregate results: include non-identical diffs and counts.

## Caching
- Cache Azure DevOps org/project/repo in `.sc/roslyn-diff/settings.json`.
- Store defaults like `files_per_agent` when set explicitly.

## Output Contract
- Always return fenced JSON with a discriminated union: `success: true|false`.
- `success: true` includes aggregated counts and per-pair roslyn-diff JSON outputs.
