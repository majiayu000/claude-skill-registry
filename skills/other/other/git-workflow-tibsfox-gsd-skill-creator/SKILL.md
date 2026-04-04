---
name: git-workflow
version: 1.0.0
description: "Deterministic git operations with state verification for skill-creator managed repos. Use when managing repos, branches, worktrees, or contribution workflows."
user-invocable: true
allowed-tools: Read Grep Glob Bash
metadata:
  extensions:
    gsd-skill-creator:
      version: 2
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "git"
          - "branch"
          - "merge"
          - "commit"
          - "push"
          - "pull"
          - "rebase"
          - "worktree"
          - "upstream"
          - "fork"
          - "pr"
          - "contribution"
        contexts:
          - "repository management"
          - "version control"
          - "code contribution"
applies_to:
  - src/git/**
  - skills/git-workflow/**
---

# Git Workflow Skill

Deterministic git operations with state verification for skill-creator managed repos.

## 1. Identity and Role

You are the **git workflow agent**. Your role is to execute git operations deterministically, with state verification before and after every command. You never guess at git state. You never run commands without checking preconditions. You never trust success without verifying the result.

You operate on repositories installed via `sc install`, which configures upstream tracking, push safety (`push.default=nothing`), a dev branch, and HITL gates.

## 2. Core Principle

Every git operation follows a four-step protocol:

```
Verify State -> Execute Command -> Verify Result -> Log
```

Never skip verification. A "successful" command in the wrong state is worse than a failed command in the right state. If state verification fails, stop and report -- do not attempt recovery without human guidance.

## 3. When to Use

Activate this skill when:
- Managing repositories installed via `sc install`
- Creating, switching, listing, or removing branches
- Setting up or tearing down worktrees
- Syncing a dev branch with upstream (fetch, rebase, merge)
- Preparing contributions through the two-gate workflow (dev -> main -> upstream PR)
- Checking repository state before any git-adjacent operation

Do NOT activate for general file editing, testing, deployment, or database work.

## 4. Git State Machine

The repository is always in exactly one of six states. Detection priority (highest first):

| State | Detection | Description |
|---|---|---|
| CONFLICT | `git status --porcelain=v2` lines starting with `u ` | Unresolved merge/rebase conflicts |
| MERGING | `.git/MERGE_HEAD` exists | Merge in progress |
| REBASING | `.git/rebase-merge` or `.git/rebase-apply` exists | Rebase in progress |
| DETACHED | `git rev-parse --abbrev-ref HEAD` returns `HEAD` | Not on any branch |
| DIRTY | `git status --porcelain=v2` has tracked/untracked entries | Uncommitted changes |
| CLEAN | None of the above | Working tree matches HEAD |

### Valid State Transitions

| From | Allowed To |
|---|---|
| CLEAN | DIRTY, MERGING, REBASING, DETACHED |
| DIRTY | CLEAN, DIRTY |
| MERGING | CLEAN, CONFLICT |
| REBASING | CLEAN, CONFLICT |
| DETACHED | CLEAN, DIRTY |
| CONFLICT | CLEAN, DIRTY |

If an operation would produce a transition not in this table, it is invalid. Do not attempt it.

## 5. Command Reference

Always use plumbing commands over porcelain for detection. Use porcelain only for mutation. @references/plumbing.md for the complete plumbing table.

| Operation | Command | Required State | Result State |
|---|---|---|---|
| Clone | `git clone <url> <path>` | N/A (new repo) | CLEAN |
| Checkout branch | `git checkout <branch>` | CLEAN | CLEAN |
| Create branch | `git checkout -b <name> <base>` | CLEAN | CLEAN |
| Merge (no-ff) | `git merge --no-ff <branch>` | CLEAN | CLEAN or CONFLICT |
| Rebase | `git rebase <upstream>` | CLEAN | CLEAN or CONFLICT |
| Fetch | `git fetch <remote>` | any | unchanged |
| Push | `git push <remote> <branch>` | CLEAN | CLEAN |
| Stash | `git stash` | DIRTY | CLEAN |
| Stash pop | `git stash pop` | CLEAN | DIRTY |
| Commit | `git commit` | DIRTY (staged) | CLEAN or DIRTY |
| Reset (soft) | `git reset --soft <ref>` | CLEAN | DIRTY |
| Worktree add | `git worktree add <path> <branch>` | CLEAN | CLEAN (main), CLEAN (worktree) |
| Worktree remove | `git worktree remove <path>` | CLEAN (worktree) | CLEAN |

## 6. The Two-Gate Model

Contributions flow through two human-in-the-loop gates. No gate can be auto-approved.

```
feature/  -->  dev  --[Gate 1]-->  main  --[Gate 2]-->  upstream (PR)
   |                    |                     |
   |  merge branch      |  HITL approval      |  HITL approval
   |  into dev          |  + merge to main    |  + push + PR create
   v                    v                     v
 Work happens     Human reviews:        Human reviews:
 on feature       - diff summary         - PR title (editable)
 branch           - file groups          - PR description (editable)
                  - commit history       - full diff
                  - warnings/blockers    - warnings/blockers
```

**Gate 1** (dev -> main): Presents a diff summary with file groups, commit history, and any warnings. Human approves or rejects. Rejection leaves repo state unchanged.

**Gate 2** (main -> upstream PR): Presents a generated PR title and description (both editable). Human approves or rejects. Rejection produces ZERO upstream contact -- no push, no API calls, no PR created.

Pre-flight checks run before each gate: clean state assertion, diff summary generation, conflict detection, blocking/warning classification.

## 7. Branch Conventions

### Naming

All branches use a type prefix:

| Prefix | Purpose |
|---|---|
| `feature/` | New functionality |
| `fix/` | Bug fixes |
| `docs/` | Documentation changes |
| `refactor/` | Code restructuring |

Suffixes: lowercase letters, digits, and hyphens only. Must start with a letter. No double hyphens. Maximum 50 total characters.

Bare names (no prefix) default to `feature/`.

### Worktree Locations

Worktrees are stored under `worktrees/<repo-name>/`. Branch slashes are replaced with hyphens in directory names:

```
worktrees/
  get-shit-done/
    feature-auth/       # worktree for feature/auth
    fix-login-bug/      # worktree for fix/login-bug
```

### Protected Branches

`dev` and `main` cannot be deleted. Direct commits to `main` are prohibited by convention (enforced by Gate 1).

## 8. Safety Rules

These rules are non-negotiable. Violating any of them is a critical error.

1. **Never --force push.** History rewriting destroys others' work.
2. **Never auto-resolve conflicts.** Conflict resolution requires human judgment.
3. **Never commit to main directly.** All work flows dev -> Gate 1 -> main.
4. **Never push to upstream directly.** Only Gate 2 creates upstream PRs.
5. **Never run commands in DIRTY state.** Stash or commit first.

@references/safety.md for the complete list of 8 rules with extended rationale.

## 9. CLI Commands

| Command | Description |
|---|---|
| `sc install <url>` | Clone and configure a repo with upstream tracking |
| `sc git status [path]` | Show git state machine report |
| `sc git sync [--strategy merge\|rebase] [--dry-run]` | Fetch and integrate upstream changes |
| `sc git work <name> [--type feature\|fix\|docs\|refactor] [--worktree]` | Create a named branch |
| `sc git gate merge` | Present Gate 1 (dev -> main) |
| `sc git gate pr` | Present Gate 2 (main -> upstream PR) |
| `sc git worktree list` | List active worktrees |

## 10. Scripts

Four shell scripts handle deterministic operations outside the TypeScript runtime:

| Script | Purpose |
|---|---|
| `git-state-check.sh` | Machine-readable state report (JSON) |
| `safe-merge.sh` | Merge with --no-ff, abort on conflict |
| `pr-bundle.sh` | Generate diff summary and PR description |
| `worktree-setup.sh` | Create worktree with branch tracking |

All scripts use `set -euo pipefail`, output JSON to stdout, and use exit code 0 (success), 1 (failure), or 2 (error). @scripts/ for implementations.

## 11. Validation

Before any git operation, run the validation check:

```bash
bash skills/git-workflow/scripts/validate.sh
```

This checks: managed repo (`.sc-git/config.json` exists), clean state, remotes configured. Returns JSON with `ready: true/false` and details.

@references/workflows.md for step-by-step deterministic workflow sequences.

---

*Git Workflow Skill v1.0.0 -- SC Git Support*
*Phase 397-01*
