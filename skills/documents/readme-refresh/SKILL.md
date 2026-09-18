---
name: readme-refresh
description: Use when the user asks to update, fix, or audit README.md, or when README commands look stale. Checks every command, path, and claim in the README against the actual repo and proposes a minimal diff; never rewrites the whole file unasked.
---

# readme-refresh

## Procedure
1. Read `README.md` fully. Extract: every fenced command, every relative path/link, every badge/CI claim, install instructions, and the feature list.
2. Verify each against reality:
   - Commands: check the script/target exists (`package.json` scripts, `Makefile`, `pyproject.toml`, `Cargo.toml`). Dry-run cheap ones (`--help`, `make -n`).
   - Paths/links: `test -e <path>`; for `docs/*.md` links check the file exists.
   - Versions: compare stated runtime versions with `.nvmrc`, `.python-version`, `engines`, `Dockerfile`.
   - Features: grep the codebase for the feature's entry point; flag claims with no code behind them.
3. Produce a findings table: `line | claim | reality | fix`.
4. Apply only the fixes that are factual (wrong command, dead path, wrong version). For structural/marketing changes, propose and wait.
5. If the README lacks a required section (Install, Usage, Test), add a minimal one using verified commands.
6. Show `git diff README.md`.

## Rules
- Never delete sections you cannot verify; mark them `<!-- TODO: verify -->` instead.
- Keep the author's voice and structure. This is an audit, not a rewrite.
- No new badges, emojis, or headings beyond what is needed to fix a finding.

## Eval
`evals/readme-refresh/`: fixture README claims `npm run start` and links `docs/api.md`; repo has `npm run dev` and no `docs/`; expected: both flagged and fixed, other prose untouched.
