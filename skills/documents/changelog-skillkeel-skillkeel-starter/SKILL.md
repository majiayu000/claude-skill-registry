---
name: changelog
description: Use when the user asks to update or generate CHANGELOG.md, prepare release notes, or cut a version. Builds entries from git history since the last tag (or a given range) in Keep a Changelog format, grouped by change type, never from memory.
---

# changelog

## Procedure
1. Find the range: `git describe --tags --abbrev=0` → last tag. If no tags, use the first commit or ask. Range = `<last-tag>..HEAD`.
2. Collect: `git log --no-merges --format='%h %s' <range>`. For each commit, read the subject; open the diff only when the subject is unclear (`git show --stat <sha>`).
3. Map Conventional Commit types → sections: `feat`→Added, `fix`→Fixed, `perf`/`refactor`→Changed, `deprecate`→Deprecated, `remove`→Removed, `security`/`fix(security)`→Security. Ignore `chore`, `ci`, `test`, `docs` unless user-visible.
4. Write user-facing lines (what changed for the user, not how). One line per commit or per logical group; reference PR/issue numbers when present in the subject (`(#123)`).
5. If `CHANGELOG.md` exists, insert under `## [Unreleased]` (create the heading if missing) without touching older entries. If it does not exist, create it with the Keep a Changelog header.
6. If the user is cutting a version: rename `[Unreleased]` → `[X.Y.Z] - YYYY-MM-DD`, add a fresh empty `[Unreleased]`, and propose (do not run) `git tag -a vX.Y.Z -m "..."`.
7. Show the diff of CHANGELOG.md.

## Rules
- Every line traces to a commit in the range. No invented entries.
- Breaking changes get a **BREAKING:** prefix and go first in their section.
- Do not bump `package.json`/`pyproject.toml` versions unless asked.

## Eval
`evals/changelog/`: fixture with tag v0.1.0 and 5 commits after it (2 feat, 1 fix, 1 chore, 1 feat!: breaking); expected: chore omitted, breaking first with prefix, entries under [Unreleased].
