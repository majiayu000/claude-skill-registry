---
name: claude-md-init
description: Use when a repo has no CLAUDE.md, or the user asks to create/refresh CLAUDE.md or project instructions for Claude Code. Generates a short, verified CLAUDE.md from the repo's real build/test/lint commands and layout, and never invents commands.
---

# claude-md-init

A good CLAUDE.md is short, true, and command-centric. Aim for 40 to 80 lines.

## Procedure
1. Inventory (read, do not guess): `ls`, `cat package.json | jq .scripts`, `Makefile` targets, `pyproject.toml` / `setup.cfg`, `Cargo.toml`, `go.mod`, `docker-compose*.yml`, `.github/workflows/*.yml` (what CI actually runs), `README.md` headings, `.editorconfig`, lint configs.
2. Verify each command you intend to list by running its cheapest, read-only form (`npm run` / `pnpm run` to list scripts, `make -n test`, `pytest --collect-only -q | tail -1`). Do not run installs or anything that writes to the tree; if a check would modify files, dry-run or skip it and say so. Drop anything that fails.
3. Detect conventions from git: `git log --format=%s -30` (commit style), branch naming, whether PRs are squashed.
4. Write `CLAUDE.md` with these sections, omitting empty ones:
   - **Project**: one sentence, stack, runtime versions (from `.nvmrc`, `.python-version`, `Dockerfile`).
   - **Commands**: install, dev, test (single test example), lint/format, build, migrate. One line each, copy-pasteable.
   - **Layout**: 5 to 10 lines mapping top-level dirs to responsibilities.
   - **Conventions**: commit style, branch naming, formatting tool, test placement, error-handling idiom if visible.
   - **Do not**: files never to edit by hand (generated, lockfiles, migrations history), commands never to run without asking (deploy, db reset).
   - **Verification**: the exact command(s) that must pass before claiming done.
5. Show the file, ask for corrections, then write it. If a CLAUDE.md already exists, propose a diff instead of overwriting.

## Rules
- Every command listed was executed or dry-run in this session. No exceptions.
- No prose about "best practices"; only facts about this repo.
- Do not include secrets, internal hostnames, or personal names.
- Keep under 100 lines; longer instructions go in `docs/` and are linked.

## Eval
`evals/claude-md-init/`: fixture: Node monorepo with `pnpm` scripts + GitHub Actions running `pnpm test:ci`; expected: CLAUDE.md lists `pnpm test:ci` (not `npm test`), notes lockfile as do-not-edit, ≤ 100 lines.
