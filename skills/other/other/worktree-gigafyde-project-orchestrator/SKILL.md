---
name: project-orchestrator:worktree
description: "Creates and manages git worktrees for parallel plan isolation. Handles monorepo (single worktree) and polyrepo (per-service worktrees) with setup auto-detection."
user-invocable: false
---

# Worktree Skill

Creates isolated git worktrees so multiple plans can be implemented in parallel without file collisions. Called by the implement command when overlap is detected, or manually via `/project:worktree`.

## Inputs

This skill expects the caller to provide:
- **slug** — the plan slug (used for branch name and worktree directory)
- **services** — list of affected service names (from the design doc's `Services Affected`)
- **design_doc_path** — absolute path to the living state doc

## Config Loading

1. Check if `.project-orchestrator/project.yml` exists in the project root
2. If yes: parse and extract:
   - `config.structure` — `monorepo` (default) or `polyrepo`
   - `config.worktree.dir` — worktree directory name (default: `.worktrees`)
   - `config.worktree.auto_detect_setup` — whether to auto-detect setup commands (default: `true`)
   - `config.services` — service definitions including `path` and optional `setup` fields
3. If no config file: assume monorepo, use all defaults

## Session Resumption

Before creating anything, check the living state doc for an existing worktree section:

1. Read the design doc at `design_doc_path`
2. Look for `## Worktree` (monorepo) or `## Worktrees` (polyrepo) section
3. If found:
   - Extract recorded path(s) and branch(es)
   - Verify worktree exists on disk: run `git worktree list` and check if the path appears
   - If missing on disk: run `git worktree prune` to clean stale entries, then fall through to creation below
   - If present: verify correct branch with `cd {worktree_path} && git branch --show-current`
     - If branch matches: return the existing path(s) — done, no creation needed
     - If branch mismatch: warn the caller — "Worktree at {path} is on branch {actual}, expected {expected}. Please investigate before proceeding." Do NOT silently proceed or switch branches.
4. If no worktree section found: proceed to creation

## Monorepo Path

When `config.structure` is `monorepo` (or absent/default):

### 1. Determine Worktree Directory

```
worktree_dir = config.worktree.dir or ".worktrees"
worktree_path = {project_root}/{worktree_dir}/{slug}
```

### 2. Gitignore Safety

Before creating the worktree:

1. Run `git check-ignore -q {worktree_dir}` from project root
2. If exit code 0: already ignored, proceed
3. If exit code 1 (not ignored):
   - Check if `.gitignore` exists and already contains a `{worktree_dir}` line (handles race with concurrent sessions)
   - If not present: append `{worktree_dir}` to `.gitignore` (create the file if needed)
   - Commit the `.gitignore` change: `git add .gitignore && git commit -m "chore: add {worktree_dir} to .gitignore"`

### 3. Branch-Aware Worktree Creation

```bash
# Check if branch already exists
git branch --list "feature/{slug}"

# If branch exists (output is non-empty):
git worktree add {worktree_path} "feature/{slug}"

# If branch does not exist:
git worktree add {worktree_path} -b "feature/{slug}"
```

**If `git worktree add` fails:** Report the error to the caller with the full error output. Suggest options:
1. Fix manually and retry
2. Proceed without a worktree

Do NOT silently fall back to working in the main tree. Let the caller (implement command) decide.

### 4. Run Setup Commands

For each affected service, run setup inside the worktree:

```
For each service in the affected services list:
  service_path = config.services[name].path or name
  setup_dir = {worktree_path}/{service_path}
  setup_cmd = determine setup command (see Setup Detection below)

  If setup_cmd found:
    cd {setup_dir} && {setup_cmd}
```

**If setup fails for a service:**
- Show the error output to the user
- Ask: "Setup failed for {service}. Continue without setup, or abort worktree creation?"
- If abort: clean up with `git worktree remove --force {worktree_path}` and report failure to caller

### 5. Post-Setup Verification

For each affected service, verify the worktree is usable:

```
For each service in the affected services list:
  service_path = config.services[name].path or name
  service_dir = {worktree_path}/{service_path}

  1. Verify directory exists: ls {service_dir}
     - Fail message: "Service directory {service_dir} not found in worktree"

  2. Verify git is healthy: cd {worktree_path} && git status --porcelain
     - Should not error. Output content is fine (unstaged changes are expected).

  3. Verify setup artifacts (Node projects only):
     - If package.json exists in {service_dir}: check node_modules/ exists
       AND is non-empty (contains at least one subdirectory)
     - Fail message: "node_modules/ missing or empty — package install may
       have failed silently. Try re-running setup."
     - For all other ecosystems: skip artifact verification.
       Setup command exit code is sufficient.

  4. If any check fails:
     - Report the error to the user
     - Ask: "Continue with potentially broken worktree, re-run setup,
       or abort worktree creation?"
     - If abort: clean up with `git worktree remove --force {worktree_path}`
       and report failure to caller
```

### 6. Record in Living State Doc

Append to the design doc (before the `---` separator or at the end):

```markdown
## Worktree
- **Path:** {absolute_worktree_path}
- **Branch:** feature/{slug}
```

### 7. Return Result

Return the absolute worktree path to the caller.

## Polyrepo Path

When `config.structure` is `polyrepo`:

### 1. Process Each Affected Service

For each service in the affected services list:

```
service_config = config.services[name]
service_repo_path = {project_root}/{service_config.path}
worktree_dir = config.worktree.dir or ".worktrees"
worktree_path = {service_repo_path}/{worktree_dir}/{slug}
```

#### a. Gitignore Safety (per repo)

Same as monorepo gitignore check, but run inside each service repo directory:

1. `cd {service_repo_path} && git check-ignore -q {worktree_dir}`
2. If not ignored: add to that repo's `.gitignore` and commit

#### b. Branch-Aware Creation (per repo)

```bash
cd {service_repo_path}

# Check if branch already exists in this repo
git branch --list "feature/{slug}"

# If exists:
git worktree add {worktree_dir}/{slug} "feature/{slug}"

# If not:
git worktree add {worktree_dir}/{slug} -b "feature/{slug}"
```

#### c. Run Setup Command (per service)

```
setup_cmd = service_config.setup or auto-detect (see Setup Detection)
If setup_cmd:
  cd {worktree_path} && {setup_cmd}
```

Collect all setup failures — do NOT prompt per-service.

#### d. Post-Setup Verification (per service)

After setup completes for a service, verify the worktree is usable:

```
service_dir = {worktree_path}

1. Verify directory exists: ls {service_dir}
   - Fail message: "Service directory {service_dir} not found in worktree"

2. Verify git is healthy: cd {worktree_path} && git status --porcelain
   - Should not error. Output content is fine (unstaged changes are expected).

3. Verify setup artifacts (Node projects only):
   - If package.json exists in {service_dir}: check node_modules/ exists
     AND is non-empty (contains at least one subdirectory)
   - Fail message: "node_modules/ missing or empty — package install may
     have failed silently. Try re-running setup."
   - For all other ecosystems: skip artifact verification.
     Setup command exit code is sufficient.
```

Collect all health check failures — do NOT prompt per-service. These get batched with setup failures in step 2.

### 2. Handle Failures (Batched)

After processing all services, if any failed (creation, setup, or health check), present a single summary:

```
Worktree creation results:
  [success] backend — {absolute_path}
  [success] frontend — {absolute_path}
  [failed]  admin — setup failed: {error message}

Options:
1. Continue with successful worktrees, implement failed services in main tree
2. Retry failed services
3. Abort all worktree creation
```

Wait for the caller's decision.

### 3. Record in Living State Doc

Append to the design doc (only successfully created worktrees):

```markdown
## Worktrees
| Service | Path | Branch |
|---------|------|--------|
| backend | {absolute_path} | feature/{slug} |
| frontend | {absolute_path} | feature/{slug} |
```

Services that failed are omitted — they will be implemented in the main service directory. Downstream commands handle this mixed state.

### 4. Return Result

Return a map of service name to absolute worktree path (only successful ones).

## Setup Detection

When a service has no explicit `setup` in config and `config.worktree.auto_detect_setup` is `true` (default), auto-detect the setup command by checking for project files in the service directory. Use the first match:

| Priority | File to Check | Setup Command |
|----------|--------------|---------------|
| 1 | `pnpm-lock.yaml` | `pnpm install` |
| 2 | `bun.lockb` | `bun install` |
| 3 | `yarn.lock` | `yarn install` |
| 4 | `package-lock.json` | `npm install` |
| 5 | `package.json` (no lockfile) | `npm install` |
| 6 | `build.gradle.kts` or `build.gradle` | `./gradlew build` |
| 7 | `Cargo.toml` | `cargo build` |
| 8 | `go.mod` | `go mod download` |
| 9 | `poetry.lock` | `poetry install` |
| 10 | `uv.lock` | `uv sync` |
| 11 | `requirements.txt` | `pip install -r requirements.txt` |
| 12 | `pyproject.toml` (no lock) | `pip install -e .` |

Check these files inside the worktree's service directory (e.g., `{worktree_path}/{service_path}/`). If none match, skip setup for that service — no warning needed.

## Error Handling

**Principle: report errors explicitly, never silently fall back.**

- **`git worktree add` fails:** Report error with full output. Suggest options (fix and retry, or proceed without). Do NOT silently work in the main tree.
- **Gitignore commit fails:** Warn the caller. The worktree can still be created, but tracked files are a risk. Let the caller decide.
- **Setup command fails (monorepo):** Ask the user per-service: continue without setup or abort worktree.
- **Setup command fails (polyrepo):** Batch all failures, present summary with options (continue partial, retry, abort all).
- **Branch already exists on wrong commit:** This is fine — `git worktree add` will use the branch as-is. The branch may have prior work from a previous session.
- **Worktree path already exists:** `git worktree add` will fail. Report the error. The user may need to run `git worktree remove` or delete the directory manually.
