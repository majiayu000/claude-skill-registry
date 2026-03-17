---
name: hk
description: "Use when bootstrapping hk pre-commit hooks for a project."
argument-hint: "[stacks... | --check | --update]"
disable-model-invocation: true
allowed-tools:
  - Glob
  - Grep
  - Read
  - Bash(command -v:*)
  - Bash(git log --oneline:*)
  - Bash(git rev-parse:*)
  - Bash(hk --version:*)
  - Bash(hk check:*)
  - Bash(hk validate:*)
  - Bash(mise --version:*)
  - Bash(mise ls-remote:*)
  - Bash(mise registry:*)
  - Bash(mise which:*)
  - Bash(test -d:*)
  - Bash(test -f:*)
---

# hk — Pre-commit Hook Bootstrap

## Arguments
```
$ARGUMENTS
```

## Pre-computed Context

```
Git repo root: !`git rev-parse --show-toplevel 2>/dev/null || echo "NOT A GIT REPO"`
hk.pkl exists: !`test -f hk.pkl && echo "yes" || echo "no"`
hk available: !`command -v hk 2>/dev/null && hk --version 2>/dev/null || echo "not installed"`
mise available: !`command -v mise 2>/dev/null && mise --version 2>/dev/null || echo "not installed"`
Conventional commits: !`git log --oneline -10 2>/dev/null || echo "no git history"`
```

## Constraints

- **Always call `EnterPlanMode` before making any changes.** This skill is plan-first — detection and analysis happen before any writes.
- Never use `git -C <path>` — it rewrites the command prefix, breaking `allowed-tools` pattern matching and forcing unnecessary user approval.
- If hk is not installed (pre-computed context shows "not installed"), the plan MUST include `mise use hk` as the first install step.
- **Always use `--mise` flags**: `hk init --mise` (scaffolds mise.toml with hk task) and `hk install --mise` (hooks execute via `mise x` so tools are in PATH without shell activation).

### allowed-tools rationale

Detection and validation tools are auto-allowed (Read, Glob, Grep, `hk validate`, `hk check`, etc.). Mutating operations — `mise use`, `hk install`, `hk fix`, Write, Edit — are **not** in `allowed-tools`, so Claude Code will prompt the user to approve each one. This is the intended flow: the agent proceeds through install/write/fix steps normally, and the user gates each action via Claude Code's standard approval UI.

## Instructions

### Parse Arguments

Determine the mode from arguments:

| Pattern | Mode |
|---------|------|
| (empty) | **Auto-detect**: scan project, detect stacks, full bootstrap |
| `--check` | **Check**: validate existing `hk.pkl`, run `hk check --all` |
| `--update` | **Update**: detect new stacks, propose additions to existing `hk.pkl` |
| `rust shell go ...` | **Force stacks**: use specified stacks, skip auto-detection |

### Mode: --check

If arguments contain `--check`:

1. Verify `hk.pkl` exists — error if not
2. Run `hk validate` to check config syntax
3. Run `hk check --all` to run all checks
4. Report results — do NOT enter plan mode
5. If failures found, suggest `hk fix --all` or `/hk --update`

### Mode: Auto-detect / Force / Update

#### 1. Immediately Enter Plan Mode

Call `EnterPlanMode` now. All remaining work happens in plan mode.

#### 2. Detect Stacks

Probe for indicator files to determine which stacks apply:

| Indicator | Stack | Stack File |
|-----------|-------|------------|
| *(always)* | essential | `stacks/essential.md` |
| `*.sh`, `*.bash`, `bin/` with scripts | shell | `stacks/shell.md` |
| `.github/workflows/*.yml` | github-actions | `stacks/github-actions.md` |
| `Cargo.toml` | rust | `stacks/rust.md` |
| `go.mod` | go | `stacks/go.md` |
| `Dockerfile*`, `Containerfile*`, `docker-compose.yml`, `compose.yml` | docker | `stacks/docker.md` |
| `*.pkl`, `PklProject`, `**/*.yml` (non-GHA) | config-languages | `stacks/config-languages.md` |
| `*.lua`, `.stylua.toml`, `init.lua` | lua | `stacks/lua.md` |

For **force stacks** mode: use only the specified stacks (plus essential always).

For **update** mode: detect stacks not already covered in existing `hk.pkl`.

#### 3. Read Stack Files

Read each detected stack's `.md` file from the `stacks/` directory (relative to this skill). Extract:
- Builtin names and `Builtins.xxx` syntax
- Tool install commands
- Gotchas and overrides
- Example pkl snippets

#### 4. Analyze Project Context

Check for additional context that affects configuration:
- Does `.editorconfig` exist? (affects editorconfig-checker, shfmt)
- Does `action.yml` exist? (affects ghalint_action)
- Are there `.tmpl` files? (affects shell stack exclusions)
- Is this a chezmoi repo? (template exclusions needed)
- Does the project use conventional commits? (check pre-computed context git log, or look for `commitlint`, `.commitlintrc`)
- What YAML files exist outside `.github/`? (affects yaml linter inclusion)
- Are there JSONC files? (`.json` files with `//` comments — VS Code/Cursor configs). Exclude from jq.
- Are there reference/vendor directories? (`docs/reference/`, `vendor/`, gitingest dumps). Exclude from content-sensitive checks (`detect-private-key`, `markdown-lint`).
- Are there other projects nested in subdirectories with their own `hk.pkl`? Add them to the global `exclude`.

#### 5. Fetch Latest hk Version

```bash
mise ls-remote hk | tail -1
```

Use the result for the `amends` line in `hk.pkl`.

#### 6. Compose hk.pkl

Mentally compose the `hk.pkl` config following this structure:

```pkl
amends "package://github.com/jdx/hk/releases/download/vX.Y.Z/hk@X.Y.Z#/Config.pkl"
import "package://github.com/jdx/hk/releases/download/vX.Y.Z/hk@X.Y.Z#/Builtins.pkl"

local linters = new Mapping<String, Step | Group> {
  // essential builtins
  // stack-specific builtins with overrides from gotchas
}

hooks = new {
  ["pre-commit"] {
    fix = true
    stash = "git"
    steps = linters
  }
  ["pre-push"] {
    steps = linters
  }
  ["check"] {
    steps = linters
  }
  ["fix"] {
    fix = true
    steps = linters
  }
}
```

If conventional commits detected, add:
```pkl
  ["commit-msg"] {
    steps {
      ["check-conventional-commit"] = Builtins.check_conventional_commit
    }
  }
```

#### 7. Present Plan

Write the plan including:
1. **Detected stacks** — list each with confidence level
2. **Proposed `hk.pkl`** — full file content, including global `exclude` for nested projects
3. **Tools to install** — exact `mise use tool@VERSION` commands (resolve versions via `mise ls-remote`)
4. **Gotchas noted** — any stack-specific warnings that apply
5. **Config files needed** — `.markdownlint.json`, `.stylua.toml`, `.editorconfig`, etc.
6. **Commit strategy** — the exact sequence of commits:
   - Commit 1: config files (`hk.pkl`, `.mise.toml`, `.markdownlint.json`, `.stylua.toml`, etc.)
   - Commit 2: `hk fix --all` auto-formatted changes to tracked files
   - Commit 3: manual fixes for hook-blocking issues (e.g., ghalint workflow hardening)

Call `ExitPlanMode` and wait for approval.

#### 8. After Approval — Execute

Run these steps in order:

1. **Install tools one at a time** with pinned versions:
   ```bash
   mise use hk@X.Y.Z
   mise use ghalint@X.Y.Z
   # etc. — one tool per command to avoid partial failures
   ```
   After each install, verify it landed in the project `.mise.toml` (not global config).
   Use `mise x -- TOOL --version` if the tool isn't in PATH yet (avoids shell reload).

   If the project has no `.mise.toml` yet, run `mise x -- hk init --mise` after installing hk
   to scaffold a mise.toml with an hk pre-commit task definition.

2. **Write config files** — `hk.pkl`, `.markdownlint.json`, `.stylua.toml`, etc.

3. **Install hooks** (with mise integration):
   ```bash
   mise x -- hk install --mise
   ```
   The `--mise` flag makes hooks execute via `mise x`, so all mise-managed tools are
   automatically in PATH — other developers don't need mise activated in their shell.

4. **Validate config**:
   ```bash
   mise x -- hk validate
   ```

5. **Run checks**:
   ```bash
   mise x -- hk check --all
   ```

6. **If check failures**, offer to fix:
   ```bash
   mise x -- hk fix --all
   ```
   Then re-run `hk check --all` to verify.

7. **Commit in sequence** (per the plan's commit strategy):
   - Commit 1: config files only
   - Commit 2: auto-formatted changes from `hk fix`
   - Commit 3: manual fixes (e.g., ghalint workflow hardening) if needed

8. **Report results** — summarize what was installed, configured, and any remaining issues.
