---
name: changelog-keepachangelog-update
description: Update an existing CHANGELOG.md using Keep a Changelog 1.0.0 format based on current repository changes. Use when users ask to update changelog entries, prepare release notes from git diff/status, maintain an Unreleased section, or keep changelog content aligned with actual code changes without inventing facts.
---

# Changelog Keep a Changelog Update

Use this workflow to update `CHANGELOG.md` from current repository changes in a deterministic and evidence-based way.

Reference format: https://keepachangelog.com/en/1.0.0/

## Workflow
1. Resolve target file and scope.
2. Collect current changes from git evidence.
3. Map evidence to Keep a Changelog categories.
4. Update `CHANGELOG.md` without fabricating details.
5. Verify structure, links, and consistency.

## 0) Resolve scope (required)
- If `CHANGELOG.md` exists at repository root, update it.
- If the user specifies another changelog path, honor that path.
- If no changelog file exists, ask one clarification question before creating a new file.
- Never update unrelated markdown files as fallback.

## 1) Collect evidence (required)
Use repository facts only:
- `git status --short` for changed files.
- `git diff --name-only` for touched paths.
- `git diff` / `git log --oneline` for behavior-level context.
- Existing `CHANGELOG.md` headings and version link style.

Do not claim behavior changes that cannot be traced to code or commit evidence.

## 2) Classify changes (required)
Map each verified change to these sections under `[Unreleased]`:
- `Added`
- `Changed`
- `Deprecated`
- `Removed`
- `Fixed`
- `Security`

Rules:
- Prefer concise, user-facing entries.
- Group related file-level changes into one logical bullet.
- Omit empty categories unless the file already keeps empty headings intentionally.

## 3) Update rules (required)
- Preserve existing heading order and version history.
- Ensure `[Unreleased]` exists near the top.
- Insert new bullets under the correct category in `[Unreleased]`.
- Keep markdown clean and consistent with existing style.
- If uncertainty remains, add `TBD (owner needed)` instead of guessing.

Version/date example (Keep a Changelog style):

```markdown
## [Unreleased]

### Added
- Add validation for missing target paths before write operations.

## [1.2.0] - 2026-02-24

### Added
- Add `changelog-keepachangelog-update` skill with deterministic update workflow.

### Changed
- Improve README governance sections for ownership and escalation visibility.
```

## 4) Verification gates
Before final output, verify:
- Keep a Changelog structure remains valid for the file's style.
- No duplicate bullets for the same change.
- All new entries are evidence-backed.
- Existing historical versions are unchanged unless explicitly requested.

## Output contract
Return:
- Updated changelog path.
- Short summary of added/changed/fixed/security entries.
- Any unresolved `TBD (owner needed)` items.
