---
name: worktree
description: >
  Use when starting feature work that needs workspace isolation — creates git worktree
  with automatic project setup and baseline test verification. Ensures worktree directory
  is git-ignored and safe. Integrates with code-forge:impl and code-forge:finish.
---

# Code Forge — Worktree

Create an isolated git worktree for feature development with automated project setup and safety verification.

## When to Use

- Starting feature work that should not affect the main workspace
- Before running code-forge:impl to isolate implementation changes
- When you need a clean baseline for testing or experimentation

## Iron Law

**NEVER create a project-local worktree without verifying it is git-ignored.** Worktree contents tracked by git will cause repository corruption.

## Workflow

```
Detect Directory → Verify Safety → Create Worktree → Project Setup → Baseline Tests → Report
```

### Step 1: Detect Worktree Directory

Check in order:
1. Existing `.worktrees/` or `worktrees/` directory in project root — use if found
2. Project CLAUDE.md for worktree preference — use without asking
3. Ask user:
   - **Project-local** `.worktrees/` (Recommended) — keeps worktrees near the code
   - **Global** `~/.config/code-forge/worktrees/` — outside project, no .gitignore needed

### Step 2: Verify Safety (Project-Local Only)

**CRITICAL:** If using a project-local directory:

```bash
git check-ignore -q <worktree-dir>
```

- **Ignored:** Proceed
- **NOT ignored:** Add to `.gitignore` immediately, then commit:
  ```bash
  echo "<worktree-dir>/" >> .gitignore
  git add .gitignore && git commit -m "chore: add worktree directory to .gitignore"
  ```

Global directory: skip this step.

### Step 3: Create Worktree

```bash
# Detect project name
PROJECT_NAME=$(basename "$(git rev-parse --show-toplevel)")

# Create worktree with new branch
git worktree add <worktree-dir>/<feature-name> -b <feature-name>
```

Branch naming: use the feature name provided by the user, prefixed with `feat/` if not already prefixed.

### Step 4: Project Setup

Auto-detect and run setup in the worktree directory:

| Marker | Command |
|--------|---------|
| `package.json` | `npm install` |
| `package-lock.json` | `npm ci` |
| `yarn.lock` | `yarn install` |
| `pnpm-lock.yaml` | `pnpm install` |
| `requirements.txt` | `pip install -r requirements.txt` |
| `pyproject.toml` | `pip install -e .` or `poetry install` |
| `Cargo.toml` | `cargo fetch` |
| `go.mod` | `go mod download` |
| `build.gradle` | `./gradlew dependencies` |
| `pom.xml` | `mvn dependency:resolve` |

If multiple markers exist, run the most specific one. If none match, skip setup.

### Step 5: Baseline Tests

Run the project's test command to establish a clean baseline:

```bash
# Auto-detect test command from package.json, Makefile, etc.
# Run tests and report results
```

- **All pass:** Report green baseline, proceed
- **Some fail:** Warn user — "Baseline has N failing tests. These are pre-existing, not caused by your changes."
- **No test command found:** Skip, inform user

### Step 6: Report

```
Worktree created:
  Branch:    feat/<feature-name>
  Location:  <worktree-dir>/<feature-name>
  Setup:     npm install (completed)
  Baseline:  42/42 tests passing

Next steps (code-forge workflow):
  /code-forge:impl <feature-name>    Execute implementation tasks
  /code-forge:finish                  When done, merge/PR/cleanup

Next steps (ad-hoc development):
  /code-forge:tdd                    Enforce TDD discipline
  /code-forge:finish                  When done, merge/PR/cleanup
```

## Example

```
$ /code-forge:worktree user-auth

Worktree created:
  Branch:    feat/user-auth
  Location:  .worktrees/user-auth
  Setup:     npm ci (completed)
  Baseline:  42/42 tests passing

Next steps:
  /code-forge:impl user-auth    Execute implementation tasks
  /code-forge:finish             When done, merge/PR/cleanup
```

## Cleanup

To remove a stale worktree manually: `git worktree remove <path>`. List all worktrees with `git worktree list`. The `/code-forge:finish` skill handles cleanup automatically.

## Common Mistakes

- Creating project-local worktree without checking .gitignore
- Skipping baseline tests — pre-existing failures mask new regressions
- Hardcoding setup commands instead of auto-detecting
- Proceeding when baseline tests fail without user acknowledgment
