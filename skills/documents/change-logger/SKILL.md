---
name: change-logger
description: Generate and maintain the root CHANGELOG.md in a beginner-friendly, analogy-rich format from git state or a commit range.
---

# Change Logger — quick diffs

Produce a dated, analogy-rich markdown entry in `CHANGELOG.md` so reviewers (human or model) see what moved without wading through raw diffs.

## Main use case

- Default: include committed changes since the last base marker in `CHANGELOG.md` plus current working tree edits, then record a new base marker.
- Optional: limit to staged only or a specific commit range (e.g., `main..HEAD`).
- Output: grouped by the first two path segments (e.g., `skills/brave-search`) with A/M/D/R counts and short analogies.

## Commands

- Show help: `./scripts/change-logger.ts --help`
- Working tree (staged + unstaged): `./scripts/change-logger.ts`
- Staged only: `./scripts/change-logger.ts --staged`
- Commit range: `./scripts/change-logger.ts --range main..HEAD`
- Custom section title: `./scripts/change-logger.ts --title "Landing page polish"`

## Notes

- Requires git in PATH and a repository context.
- Ignored dirs follow git defaults; handles renames via git diff output.
- Writes/updates `CHANGELOG.md` at the repo root with dated sections and analogies; ideal for PRs, oracle prompts, or release notes.
- The base commit marker is stored in each new changelog section and used on subsequent runs to avoid re-listing old commits.
