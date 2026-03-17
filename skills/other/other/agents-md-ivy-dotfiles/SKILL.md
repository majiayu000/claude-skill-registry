---
name: agents-md
description: "Use when asked to create or update an AGENTS.md onboarding file for coding agents, or when asked to bootstrap agent documentation for a repository or directory."
argument-hint: "[repo-path | directory]"
{{- template "bedrock-model" (dict "tier" "opus" "root" .) }}
allowed-tools:
  - Bash(file:*)
  - Bash(ls:*)
  - Bash(readlink:*)
  - Bash(test -L:*)
  - Bash(test -e:*)
  - Bash(test -f:*)
  - Bash(tree:*)
  - Glob
  - Grep
  - Read
---

# AGENTS.md Generator

You are a coding agent working inside THIS repository. Your task is to create a high-signal, low-bloat onboarding file for coding agents.

## Arguments

```
$ARGUMENTS
```

If arguments include a path, `cd` there first. Otherwise, operate on the current working directory.

## Pre-computed Context

The following checks ran before this skill was invoked:

**AGENTS.md exists:** !`test -f AGENTS.md && echo "yes" || echo "no"`
**CLAUDE.md exists:** !`test -e CLAUDE.md && echo "yes" || echo "no"`
**CLAUDE.md is symlink:** !`test -L CLAUDE.md && echo "yes" || echo "no"`
**CLAUDE.md symlink target:** !`readlink CLAUDE.md 2>/dev/null || echo "(not a symlink or does not exist)"`
**AGENTS.local.md exists:** !`test -f AGENTS.local.md && echo "yes" || echo "no"`

Use this context to skip redundant checks. If CLAUDE.md is already a symlink pointing to AGENTS.md, don't recreate it.

## Deliverables

1. Create (or update) a root-level file named `AGENTS.md`.
2. Create (or update) a root-level symlink `CLAUDE.md` that points to `AGENTS.md`.

## Core Principles (do not violate)

- **Assume the model is stateless**: every session starts with zero repo knowledge.
- **Less is more**: include ONLY universally applicable info. If it won't help for most tasks, don't put it in `AGENTS.md`.
- **Prefer pointers over copies**: avoid code snippets and long lists. Prefer `see path/to/document.md` references.
- **Progressive disclosure**: if deeper, task-specific guidance is needed, point to (or create) separate small docs under `docs/agents/` with self-descriptive names. `AGENTS.md` should index those docs, not duplicate them.
- **Don't use the agent as a linter**: don't paste style guides. Rely on existing formatters/linters and show only the canonical commands to run them.
- **Keep it concise**: aim for <150 lines, hard cap 300 lines.

## Workflow

### 1. Repo Discovery

Use the tools you have: filesystem, grep, tree, package managers, etc.

- Read root README and any top-level docs to understand the project's purpose and structure.
- Identify the "source of truth" for build/test/run commands:
  - `package.json` scripts / pnpm-workspace / turbo / nx / bun
  - `Makefile`
  - `pyproject.toml` / `tox.ini`
  - `go.mod` / magefile
  - `docker-compose` / `justfile` / `taskfile`
  - CI config (GitHub Actions, Buildkite, etc.) for canonical checks
- Identify monorepo layout (`apps/`, `packages/`, `services/`, `libs/`, etc.) and what each is for.
- Identify "gotchas" that matter broadly (required env vars, bootstrap steps, codegen, DB migrations, local stack).
- Check if `AGENTS.md` (or `CLAUDE.md`) already exists. If it does, proceed to step 1b. Otherwise, skip to step 2.

### 1b. Fact-check Existing AGENTS.md

When an `AGENTS.md` already exists, audit it against the actual repo state before making changes.

**Verify each claim:**

- **Commands**: Run or inspect every build/test/lint/dev command mentioned. Do they still work? Do the scripts/targets exist?
- **File paths & pointers**: Confirm every referenced file, directory, and doc link actually exists at the stated path.
- **Directory structure**: Compare the documented repo map against the real `tree`/`ls` output. Identify added, removed, or renamed directories.
- **Tool versions & prerequisites**: Check that mentioned tools, runtimes, and env vars match current config files (`package.json`, `pyproject.toml`, `.mise.toml`, `Dockerfile`, etc.).
- **CI/CD references**: Verify CI workflow names, job names, and check sequences against actual workflow files.
- **Stale content**: Identify sections that reference removed features, deprecated commands, or old patterns no longer in use.

**Revision rules:**

- Fix factual errors in-place (wrong paths, renamed commands, missing dirs).
- Remove references to things that no longer exist.
- Add coverage for significant new directories, commands, or workflows not yet documented.
- Preserve the author's voice and structure -- don't rewrite sections that are accurate.
- Apply the same Core Principles (conciseness, pointers over copies, progressive disclosure) when adding new content.
- In your final summary, list every change with a short rationale (e.g., "Fixed: `npm test` -> `pnpm test` (`package.json` uses pnpm)").

After fact-checking, skip to step 3 (implementation details).

### 2. Write AGENTS.md (new file only)

Follow THIS structure (keep each section short and skimmable):

1. **Purpose (WHY)** -- 2-5 bullets
   - What this repo is for, and what success looks like.

2. **Repo map (WHAT)** -- compact directory map
   - Top-level directories + one-line descriptions.
   - If monorepo: list key apps/packages and how they relate.

3. **How to work here (HOW)** -- the minimum commands that actually matter
   - **Setup/bootstrap**: the single best "first command".
   - **Build**: canonical command(s).
   - **Test**: canonical command(s) (unit/integration/e2e if truly standard).
   - **Typecheck/lint/format**: canonical command(s) (no rule lists).
   - **Run/dev**: canonical command(s).
   - **"Verify before you open a PR"**: the shortest reliable check sequence.

   > **Notes:**
   > - Prefer referencing existing scripts (`see path/to/package.json`) over duplicating many commands.
   > - If multiple stacks exist, give a tiny "most common path" + pointers for the rest.

4. **Change hygiene** -- universal expectations (max ~8 bullets)
   - Examples: keep diffs small, add/adjust tests, follow existing patterns, don't do repo-wide reformatting, don't commit secrets, explain tradeoffs in PR description, etc.

5. **Progressive disclosure index (`docs/agents/`)**
   - Create `docs/agents/` only if needed.
   - Add a short list like:
     - `docs/agents/running-tests.md` -- deeper test matrix (read when modifying CI/tests)
     - `docs/agents/service-architecture.md` -- service boundaries (read when changing APIs)
   - Each doc should be short, pointer-heavy, and avoid code duplication.

6. **"Where to look first"** (2-6 bullets)
   - The few best files/dirs for common tasks (e.g., config, main entrypoints, API definitions).

### 3. Implementation Details (files + symlink)

- Write `AGENTS.md` where specified.
- If `AGENTS.local.md` exists, include `@AGENTS.local.md` near the top of the file (e.g. right after the title or introduction). Agents read `@`-references intuitively — no markdown link or explanation needed. Some projects provide a local `/agents-local-md` skill to generate this file — if the project has one, suggest running it.
- Create/update the symlink so `CLAUDE.md` -> `AGENTS.md` (relative symlink).
- If `CLAUDE.md` exists as a real file, replace it with a symlink.

### 4. Open for Human Review

After writing `AGENTS.md`, open it in a new tmux pane for the user to review and edit:

```bash
tmux split-window -h "$EDITOR AGENTS.md"
```

### 5. Quality Bar (self-check before finishing)

- Would ~80% of tasks benefit from everything in `AGENTS.md`? If not, delete or move to `docs/agents/`.
- Is it skimmable in under 60 seconds?
- Did you avoid long command menus, style rule dumps, and code snippets?
- Did you include the minimum set of commands to build/test/verify changes?
- Did you add precise pointers to authoritative docs/files instead of duplicating content?

## Output Requirements

- Commit-ready `AGENTS.md` content.
- Ensure `CLAUDE.md` is a symlink to `AGENTS.md`.
- In your final response, summarize what you changed and where you found the canonical commands (file paths).
