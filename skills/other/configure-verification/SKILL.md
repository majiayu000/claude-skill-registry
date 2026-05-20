---
name: configure-verification
description: Auto-detect test, lint, typecheck, and build commands from package.json, Makefile, and other project config. Use during project setup or when build tooling changes. Runs silently — no prompts.
argument-hint: [project-directory]
allowed-tools: Read, Edit, Grep, Glob, Bash
---

Auto-detect verification commands and write `.claude/verification-config.json`.
Runs silently with no user prompts — best-effort detection only.

## Workflow

```
Configure Verification Progress:
- [ ] Detect project directory and context
- [ ] Directory guard
- [ ] Detect package manager
- [ ] Auto-detect commands from project sources
- [ ] Conditional dev server detection
- [ ] Ensure .gitignore protection
- [ ] Write verification-config.json
- [ ] Output one-line summary
```

## Project Directory

Use the current working directory by default.

If `$1` is provided, treat `$1` as the working directory and read files under
`$1` instead.

## Context Detection

Determine working context:

1. If the working directory matches `*/features/*`:
   - PROJECT_ROOT = parent of parent of working directory
2. Otherwise:
   - PROJECT_ROOT = working directory

## Directory Guard

Confirm `PROJECT_ROOT` exists and is writable. If not, stop and report the error.

## Detect Package Manager

Determine package manager from lockfile presence (check in this order):

| Lockfile | Package Manager |
|----------|----------------|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `package-lock.json` | npm |

If none found, default to `npm` if `package.json` exists, otherwise no package manager.

## Auto-Detect Commands

Scan project sources in priority order. **First source wins per command type.**
Parse files as structured data (JSON for package.json, not grep).

### Priority Order

1. **`package.json` scripts** — Parse JSON, check for these script names:
   - `test` → `{pm} test` or `{pm} run test`
   - `lint` → `{pm} run lint`
   - `typecheck` or `type-check` or `tsc` → `{pm} run typecheck` (use actual script name)
   - `build` → `{pm} run build`
   - `coverage` or `test:coverage` → `{pm} run coverage` (use actual script name)
   - `mutation` or `test:mutation` or `stryker` → `{pm} run {actual-script-name}`

2. **`Makefile`** — Look for targets: `test`, `lint`, `typecheck`/`check`, `build`, `coverage`
   - Command format: `make {target}`

3. **`Taskfile.yml`** — Look for tasks with matching names
   - Command format: `task {name}`

4. **`justfile`** — Look for recipes with matching names
   - Command format: `just {name}`

5. **Fallback: `README.md` / `CONTRIBUTING.md`** — Scan for code blocks containing
   test/lint/build commands. Only use if no structured source found a command.

**Important:** Only record commands that were actually found. Do not guess or
synthesize commands. If a command type is not found in any source, omit it from
the config entirely.

## Conditional Dev Server Detection

**Only run this section if** `EXECUTION_PLAN.md` contains `BROWSER:` criteria
(e.g., `BROWSER:DOM`, `BROWSER:VISUAL`, etc.).

If browser criteria exist, look for dev server scripts in `package.json`:
- `dev` → `{pm} run dev`
- `start` → `{pm} run start`
- `serve` → `{pm} run serve`

If found, include in config:
```json
{
  "devServer": {
    "command": "{pm} run dev",
    "url": "http://localhost:3000",
    "startupSeconds": 10
  }
}
```

Use port 3000 as default. If the script content in package.json contains a
different port (e.g., `--port 5173`), use that instead.

If no browser criteria in EXECUTION_PLAN.md, omit `devServer` entirely.

## Ensure .gitignore Protection

Check and protect verification-related files:

1. If `.gitignore` exists, ensure these entries are present:
   - `.env.verification`
   - `.claude/verification/auth-state.json`

2. If entries are missing, append them:
   ```
   # Verification credentials (never commit)
   .env.verification
   .claude/verification/auth-state.json
   ```

3. If `.gitignore` doesn't exist, skip (don't create one just for this).

## Write Config

Write `.claude/verification-config.json` with only the keys where commands were
found. Always include `browser.tool: "auto"`.

**Example — full detection:**
```json
{
  "commands": {
    "test": "npm test",
    "lint": "npm run lint",
    "typecheck": "npm run typecheck",
    "build": "npm run build",
    "coverage": "npm run coverage"
  },
  "browser": {
    "tool": "auto"
  }
}
```

**Example — partial detection (no typecheck or coverage found):**
```json
{
  "commands": {
    "test": "npm test",
    "lint": "npm run lint",
    "build": "npm run build"
  },
  "browser": {
    "tool": "auto"
  }
}
```

**Example — with dev server (browser criteria detected):**
```json
{
  "commands": {
    "test": "pnpm test",
    "lint": "pnpm run lint"
  },
  "devServer": {
    "command": "pnpm run dev",
    "url": "http://localhost:5173",
    "startupSeconds": 10
  },
  "browser": {
    "tool": "auto"
  }
}
```

**Example — nothing detected:**
```json
{
  "commands": {},
  "browser": {
    "tool": "auto"
  }
}
```

Do NOT include `auth`, `deployment`, or `devServer` (unless browser criteria
detected a dev server). These are deferred to `/phase-checkpoint` when needed.

## Output

Print a single summary line:

```
Verification config: detected {list of found commands}. Missing: {list of not found}.
```

Examples:
```
Verification config: detected test, lint, build. Missing: typecheck, coverage.
```
```
Verification config: detected test, lint, typecheck, build, coverage, devServer. Missing: none.
```
```
Verification config: no commands detected.
```
