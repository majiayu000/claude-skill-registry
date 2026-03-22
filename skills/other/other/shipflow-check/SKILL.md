---
name: shipflow-check
description: Run typecheck, lint, and build for the current project, then fix any errors found
disable-model-invocation: true
argument-hint: [fix|nofix]
---

## Context

- Current directory: !`pwd`
- Package manager lockfiles: !`ls -1 package-lock.json yarn.lock pnpm-lock.yaml requirements.txt Pipfile.lock 2>/dev/null || echo "none found"`
- Package.json scripts (if any): !`cat package.json 2>/dev/null | grep -E '^\s+"(dev|build|lint|typecheck|check|test|format)"' || echo "no package.json"`
- Project CLAUDE.md (if any): !`head -80 CLAUDE.md 2>/dev/null || echo "no CLAUDE.md"`

## Your task

Run all available checks for the current project and fix errors if found.

### Workspace root detection

If the current directory has no project markers (no `package.json`, no `requirements.txt`, no `src/` dir) BUT contains multiple project subdirectories — you are at the **workspace root**. Use **AskUserQuestion**:
- Question: "Which project(s) should I check?"
- `multiSelect: true`
- One option per project: label = project name, description = stack
- Read project list from `/home/claude/shipflow_data/PROJECTS.md`

Then run checks for each selected project sequentially.

### Step 0: Choose which checks to run

If `$ARGUMENTS` is empty (not "fix" or "nofix"), use **AskUserQuestion**:
- Question: "Which checks should I run?"
- `multiSelect: true`
- Options:
  - **Typecheck** — "TypeScript/Astro type validation"
  - **Lint** — "ESLint, formatting, style rules"
  - **Build** — "Full production build"
  - **Test** — "Unit/integration tests"
  - **Dependencies** — "Quick vulnerability + outdated check (run /shipflow-deps for full audit)"
- All options pre-selected by default

If `$ARGUMENTS` is "fix" or "nofix", run all detected checks (skip the prompt).

### Step 1: Detect project type and run checks

Based on the context above, identify the project stack and run the appropriate commands **sequentially** (each depends on the previous passing):

**TypeScript/JavaScript projects** (has package.json):
- Typecheck: `npm run typecheck` or `yarn typecheck` or `pnpm typecheck` (match the lockfile)
- Lint: `npm run lint` or equivalent (if script exists)
- Build: `npm run build` or `pnpm build` or `yarn build`

**Astro projects** (has astro in dependencies):
- `pnpm check` or `npm run check` (Astro type checking)
- `pnpm build` or `npm run build`

**Python projects** (has requirements.txt or Pipfile):
- `python -m py_compile` on changed files, or `pytest --co -q` (collect-only) to validate
- `pytest -x` (stop on first failure)

**Bash projects** (shell scripts, no package.json):
- `bash -n` syntax check on `.sh` files
- Run test scripts if they exist (`./test_*.sh`)

### Step 1b: Check dependencies (if selected) — quick scan only

> For comprehensive dependency auditing (unused deps, license compliance, type coverage, supply chain), run `/shipflow-deps`.

**Node.js projects** (has package.json):
- Run `npm audit --audit-level=high` / `yarn audit` / `pnpm audit` — report critical/high vulnerabilities only
- Run `npm outdated` / `yarn outdated` / `pnpm outdated` — show summary count (X patch, Y minor, Z major)

**Python projects** (has requirements.txt):
- Run `pip-audit` if available — report critical/high vulnerabilities only
- Run `pip list --outdated` — show summary count

Report a quick summary. Do NOT auto-update dependencies. Recommend `/shipflow-deps` for full analysis (unused, duplicates, licenses, configuration).

### Step 2: Fix errors

If `$ARGUMENTS` is "nofix", stop here and just report the errors.

Otherwise (default behavior, including when `$ARGUMENTS` is "fix" or empty):

1. Read each error message carefully.
2. Open the failing file(s) and fix the root cause.
3. Re-run the failed check to confirm the fix works.
4. Repeat until all checks pass or you've attempted 3 fix cycles.

### Step 3: Report

Summarize what was checked, what failed, and what was fixed. If anything still fails after 3 attempts, explain the remaining errors clearly so the user can decide what to do.

### Important

- Use the correct package manager for the project (check lockfiles).
- Do not install dependencies — if something is missing, tell the user.
- Do not modify test expectations to make tests pass. Fix the actual code.
- If the project CLAUDE.md specifies custom check commands, use those instead.
