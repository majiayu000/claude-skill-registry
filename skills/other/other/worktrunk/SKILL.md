---
name: worktrunk
description: >
  Use this skill when the user asks about Worktrunk (wt), git worktree management,
  running parallel AI agents with worktrees, setting up wt hooks, configuring wt.toml,
  using `wt switch`, `wt list`, `wt merge`, `wt remove`, `wt step`, LLM commit messages,
  or integrating Worktrunk with your AI agent. Also trigger when the user wants to run
  multiple AI agent sessions in parallel across isolated git branches, or automate
  dev server / database / dependency setup per worktree. Always use this skill for any
  question involving the `wt` CLI, worktree lifecycle automation, or the worktrunk plugin.
license: MIT
compatibility: opencode
---

# Worktrunk Skill

Worktrunk (`wt`) is a CLI for git worktree management designed to run AI agents
(like Claude Code) in parallel across isolated branches. Think of it as making
`git worktree` as easy as `git branch`.

## Quick Reference

| Task | Command |
|---|---|
| Create worktree + switch | `wt switch --create feat` |
| Create worktree + launch Claude | `wt switch --create feat -x claude` |
| List all worktrees | `wt list` |
| Merge & clean up | `wt merge main` |
| Remove current worktree | `wt remove` |
| Commit staged changes | `wt step commit` |

## Installation

```bash
# macOS/Linux (recommended)
brew install worktrunk && wt config shell install

# Cargo
cargo install worktrunk && wt config shell install

# Windows
winget install max-sixty.worktrunk
git-wt config shell install
```

Shell integration (`wt config shell install`) is required so that `wt switch`
can actually change the shell's directory.

## Core Workflow

### 1. Create and Switch

```bash
wt switch --create feature-auth         # New branch + worktree
wt switch --create feature-auth -x claude  # + launch Claude in it
wt switch existing-branch               # Switch to existing worktree
wt switch -                             # Previous worktree
```

Worktrees are placed at `../repo.branch-name` by default (configurable).

### 2. Inspect Status

```bash
wt list                    # All worktrees with status, commits, CI
wt list --full --branches  # Include remote branches without worktrees
wt list --format=json      # Machine-readable output
```

Key indicators in `wt list`:

- `@` = current worktree
- `+` / `-` = staged / unstaged changes
- `↑` / `↓` = ahead / behind remote
- `⇡` / `⇣` = ahead / behind default branch
- `🤖` = Claude is working (Claude Code plugin)
- `💬` = Claude waiting for input

### 3. Parallel Agents Pattern

```bash
wt switch -x claude -c feature-a -- 'Add user authentication'
wt switch -x claude -c feature-b -- 'Fix the pagination bug'
wt switch -x claude -c feature-c -- 'Write tests for the API'
```

`-x` / `--execute` runs a command after switching; arguments after `--` are passed to it.

### 4. Merge or Clean Up

**PR workflow:**

```bash
wt step commit              # Commit staged changes with optional LLM message
gh pr create                # Open PR
wt remove                   # After PR merged
```

**Local merge (squash + rebase + fast-forward):**

```bash
wt merge main
# Commits, rebases onto main, fast-forward merges, removes worktree
```

## Hooks

Hooks automate worktree lifecycle events. Define in `.config/wt.toml` (project)
or `~/.config/worktrunk/config.toml` (user/global).

See `references/hooks.md` for the full hook reference, template variables, and
common patterns (dev servers, databases, cold-start elimination).

### Hook Types at a Glance

| Hook | When | Blocking |
|---|---|---|
| `post-create` | After creation | Yes (blocks --execute) |
| `post-start` | After creation | No (background) |
| `post-switch` | Every switch | No |
| `pre-commit` | Before merge commit | Yes |
| `pre-merge` | Before merge | Yes |
| `post-merge` | After merge | Yes |
| `pre-remove` | Before removal | Yes |
| `post-remove` | After removal | No |

### Essential Hook Patterns

**Eliminate cold starts** (copy deps/caches/env from main):

```toml
[post-start]
copy = "wt step copy-ignored"
```

**Dev server per worktree** (deterministic port from branch name):

```toml
[post-start]
server = "npm run dev -- --port {{ branch | hash_port }}"
[pre-remove]
server = "lsof -ti :{{ branch | hash_port }} -sTCP:LISTEN | xargs kill 2>/dev/null || true"
```

**Local CI gate** (run tests before merge):

```toml
[pre-merge]
test = "npm test"
build = "npm run build"
```

## Template Variables & Filters

In hook commands (Jinja2 syntax):

| Variable | Value |
|---|---|
| `{{ branch }}` | Branch name |
| `{{ repo }}` | Repository directory name |
| `{{ worktree_path }}` | Absolute path to this worktree |
| `{{ default_branch }}` | Default branch name |
| `{{ target }}` | Target branch (merge hooks only) |

| Filter | Example | Output |
|---|---|---|
| `sanitize` | `{{ branch \| sanitize }}` | `/` and `\` → `-` |
| `sanitize_db` | `{{ branch \| sanitize_db }}` | DB-safe identifier |
| `hash_port` | `{{ branch \| hash_port }}` | Stable port 10000-19999 |

## LLM Commit Messages

Generate commit messages from diffs:

```bash
wt step commit              # Commit staged changes, generate message
wt step commit --all        # Stage all + commit
```

Configure in `~/.config/worktrunk/config.toml`:

```toml
[commit.generation]
model = "claude-opus-4-5"   # or any supported model
provider = "anthropic"
```

## Claude Code Integration

Install the plugin for activity tracking (`🤖` / `💬` in `wt list`) and
configuration skill:

```bash
claude plugin marketplace add max-sixty/worktrunk
claude plugin install worktrunk@worktrunk
```

Add to `~/.claude/settings.json` for statusline:

```json
{
  "statusLine": {
    "type": "command",
    "command": "wt list statusline --format=claude-code"
  }
}
```

## Zellij Integration

Spawn agent handoffs directly into Zellij panes (great with your existing Zellij setup):

```bash
zellij run -- wt switch --create fix-auth -x claude -- \
  'Fix the session timeout bug in auth module'
```

Or use hooks for a full multi-pane layout per worktree:

```toml
# .config/wt.toml
[post-create]
zellij = """
zellij action new-tab --name {{ branch | sanitize }}
zellij action new-pane -- claude
"""
```

## Common Commands for devops Work

For microservice's repos, a typical `.config/wt.toml`:

```toml
[post-create]
env = "cp {{ primary_worktree_path }}/.env.local .env.local 2>/dev/null || true"

[post-start]
copy = "wt step copy-ignored"

[pre-merge]
lint = "make lint"
test = "make test"

[post-merge]
notify = "echo '✓ Merged {{ branch }} → {{ target }}'"
```

## Further Reference

- `references/hooks.md` — Complete hook documentation with all patterns
- `references/commands.md` — Full command reference (switch, list, merge, remove, step, config)
- Official docs: https://worktrunk.dev
- Claude Code integration: https://worktrunk.dev/claude-code/
- Tips & patterns: https://worktrunk.dev/tips-patterns/
