---
name: ru
description: "Repo Updater - Multi-repo synchronization with AI-assisted review orchestration. Parallel sync, agent-sweep for dirty repos, ntm integration, git plumbing. 17K LOC Bash CLI."
---

# RU - Repo Updater

A comprehensive Bash CLI for synchronizing dozens or hundreds of GitHub repositories. Beyond basic sync, RU includes a full AI-assisted code review system and agent-sweep capability for automatically processing uncommitted changes across your entire projects directory.

## Why This Exists

When you work with 47+ repos (personal projects, forks, dependencies), keeping them synchronized manually is tedious. But synchronization is just the beginning—RU also orchestrates AI coding agents to review issues, process PRs, and commit uncommitted work at scale.

**The problem it solves:**
- Manual `cd ~/project && git pull` for each repo
- Missing updates that accumulate into merge conflicts
- Dirty repos that never get committed
- Issues and PRs that pile up across repositories
- No coordination for AI agents working across repos

## Critical Concepts

### Git Plumbing, Not Porcelain

RU uses git plumbing commands exclusively—never parses human-readable output:

```bash
# WRONG: Locale-dependent, version-fragile
git pull 2>&1 | grep "Already up to date"

# RIGHT: Machine-readable plumbing
git rev-list --left-right --count HEAD...@{u}
git status --porcelain
git rev-parse HEAD
```

### Stream Separation

Human-readable output goes to stderr; data to stdout:

```bash
ru sync --json 2>/dev/null | jq '.summary'
# Progress shows in terminal, JSON pipes to jq
```

### No Global `cd`

All git operations use `git -C`. Never changes working directory.

## Essential Commands

### Sync (Primary Use Case)

```bash
# Sync all configured repos
ru sync

# Parallel sync (much faster)
ru sync -j8

# Dry run - see what would happen
ru sync --dry-run

# Resume interrupted sync
ru sync --resume

# JSON output for scripting
ru sync --json 2>/dev/null | jq '.summary'
```

### Status (Read-Only Check)

```bash
# Check all repos without modifying
ru status

# JSON output
ru status --json
```

### Repo Management

```bash
# Initialize configuration
ru init

# Add repos to sync list
ru add owner/repo
ru add https://github.com/owner/repo
ru add owner/repo@branch as custom-name

# Remove from list
ru remove owner/repo

# List configured repos
ru list

# Detect orphaned repos (in projects dir but not in list)
ru prune           # Preview
ru prune --delete  # Actually remove
ru prune --archive # Move to archive directory
```

### Diagnostics

```bash
ru doctor      # System health check
ru self-update # Update ru itself
```

## AI-Assisted Review System

RU includes a powerful review orchestration system for managing AI-assisted code review across your repositories.

### ⚠️ CRITICAL SAFETY RULES - NEVER VIOLATE ⚠️

**1. NEVER Stash User Changes**
If repositories have uncommitted changes, **NEVER use `git stash`**. This risks losing user work. Stashed changes can be difficult to recover, especially untracked files which require `git show stash@{0}^3:path` to extract.

**2. NEVER Modify Working Tree Without Permission**
Do not run `git checkout`, `git reset`, `git clean`, or any command that modifies uncommitted changes without explicit user permission.

**3. Commit Changes First (The Correct Approach)**
If repos have uncommitted changes and the user wants to proceed with review, **commit the changes first** with logical groupings and detailed messages, then push.

**4. Let ru Skip Dirty Repos**
The `ru review` command automatically skips repositories with uncommitted changes. This is correct behavior—let it skip them rather than forcing them clean.

### Decision Tree: Handling Dirty Repos

```
Found uncommitted changes in repos?
├── User wants to proceed with ru review?
│   ├── YES → Ask: "Should I commit these changes first?"
│   │   ├── User says YES → Commit with logical groupings, push, then run ru review
│   │   └── User says NO → Let ru skip those repos, review clean repos only
│   └── NO → Stop, let user handle their changes
└── No uncommitted changes → Run ru review normally
```

### Two-Phase Review Workflow

**Phase 1: Discovery (`--plan`)**
- Queries GitHub for open issues and PRs across all repos
- Scores items by priority using label analysis and age
- Creates isolated git worktrees for safe review
- Spawns Claude Code sessions in terminal multiplexer

**Phase 2: Application (`--apply`)**
- Reviews proposed changes from discovery phase
- Runs quality gates (ShellCheck, tests, lint)
- Optionally pushes approved changes (`--push`)

```bash
# Discovery - see what issues/PRs exist
ru review --dry-run

# Plan mode - generate review plans, no mutations
ru review --plan

# After reviewing AI suggestions
ru review --apply --push
```

### Priority Scoring Algorithm

| Factor | Points | Logic |
|--------|--------|-------|
| **Type** | 0-20 | PRs: +20, Issues: +10, Draft PRs: -15 |
| **Labels** | 0-50 | security/critical: +50, bug/urgent: +30 |
| **Age (bugs)** | 0-50 | >60 days: +50, >30 days: +30 |
| **Recency** | 0-15 | Updated <3 days: +15, <7 days: +10 |
| **Staleness** | -20 | Recently reviewed: -20 |

Priority levels: CRITICAL (≥150), HIGH (≥100), NORMAL (≥50), LOW (<50)

### Session Drivers

| Driver | Description | Best For |
|--------|-------------|----------|
| `auto` | Auto-detect best available | Default |
| `ntm` | Named Tmux Manager integration | Multi-agent workflows |
| `local` | Direct tmux sessions | Simple setups |

```bash
ru review --mode=ntm --plan
ru review --mode=local --plan  # Use if ntm has issues
ru review -j 4 --plan          # Parallel sessions
```

### Review Options

```bash
ru review --max-repos=10 --plan       # Limit repos
ru review --max-runtime=30 --plan     # Minutes budget
ru review --skip-days=14 --plan       # Skip recently reviewed
ru review --repos=PATTERN --plan      # Filter by regex
ru review --analytics                 # View past review stats
```

### Contribution Policy

The `ru review` command includes this contribution policy in its prompts:

> We don't allow PRs or outside contributions to this project as a matter of policy. Feel free to submit issues, and even PRs if you want to illustrate a proposed fix, but know I won't merge them directly. Instead, I'll have Claude or Codex review submissions via `gh` and independently decide whether and how to address them.

**Key principle:** Independently verify and validate all user reports. Don't trust submitted fixes blindly—use them as inspiration but verify everything against actual code and documentation.

### Multi-Agent Coordination

When multiple agents review repos simultaneously:

1. **Use alphabetical ordering** - One agent works A→Z, another Z→A
2. **Check which repos are in progress** - Look for uncommitted changes or lock files
3. **Skip repos being worked on** - Don't review a repo another agent is actively modifying

### Review Response Guidelines

When reviewing issues and PRs:
- **Verify independently** - Don't trust submitted code blindly
- **Check actual behavior** - Run tests, verify against docs
- **Use gh commands** to respond on behalf of the user
- **Close issues** that are resolved or invalid
- **Request clarification** if issue is unclear

### What NOT to Do During Review

- ❌ `git stash` - NEVER stash user changes
- ❌ `git checkout -- .` - NEVER discard changes
- ❌ `git reset --hard` - NEVER reset working tree
- ❌ `git clean -fd` - NEVER clean untracked files
- ❌ Shell loops to iterate repos - ru handles iteration internally
- ❌ Direct `gh` commands for bulk operations - use ru's orchestration

### What TO Do During Review

- ✅ Use `ru review --dry-run` to discover work items
- ✅ Let ru skip repos with uncommitted changes
- ✅ Ask user before modifying their working tree state
- ✅ Commit changes (with user permission) before review if needed
- ✅ Use `--mode=local` if ntm has issues
- ✅ Work in reverse alphabetical order when coordinating with other agents

### Emergency: Recovering from Accidental Stash

If someone accidentally stashed changes:

**Tracked Files (Easy):**
```bash
git stash pop  # Restore tracked changes
```

**Untracked Files (Harder):**
```bash
# List untracked files in stash
git show stash@{0}^3 --name-only

# Extract a specific untracked file
git show stash@{0}^3:path/to/file.rs > path/to/file.rs
```

**If Stash Was Dropped:**
```bash
# Find dangling stash commits
git fsck --unreachable | grep commit

# For each commit, check if it's your stash
git show <commit-hash>

# Recover if found
git stash apply <commit-hash>
```

## Agent Sweep (Automated Dirty Repo Processing)

The `ru agent-sweep` command orchestrates AI coding agents to automatically process repositories with uncommitted changes.

### Basic Usage

```bash
# Process all repos with uncommitted changes
ru agent-sweep

# Dry run - preview what would be processed
ru agent-sweep --dry-run

# Process 4 repos in parallel
ru agent-sweep -j4

# Filter to specific repos
ru agent-sweep --repos="myproject*"

# Include release step after commit
ru agent-sweep --with-release

# Resume interrupted sweep
ru agent-sweep --resume

# Start fresh
ru agent-sweep --restart
```

### Three-Phase Agent Workflow

**Phase 1: Planning** (`--phase1-timeout`, default 300s)
- Claude Code analyzes uncommitted changes
- Determines which files should be staged (respecting denylist)
- Generates structured commit message

**Phase 2: Commit** (`--phase2-timeout`, default 600s)
- Validates the plan (file existence, denylist compliance)
- Stages approved files, creates commit
- Runs quality gates
- Optionally pushes to remote

**Phase 3: Release** (`--phase3-timeout`, default 300s, requires `--with-release`)
- Analyzes commit history since last tag
- Determines version bump (patch/minor/major)
- Creates git tag and optionally GitHub release

### Execution Modes

```bash
--execution-mode=agent  # Full AI-driven workflow (default)
--execution-mode=plan   # Phase 1 only: generate plan, stop
--execution-mode=apply  # Phase 2+3: execute existing plan
```

### Preflight Checks

Each repo is validated before spawning an agent:

| Check | Skip Reason |
|-------|-------------|
| Is git repository | `not_a_git_repo` |
| Git email configured | `git_email_not_configured` |
| Not a shallow clone | `shallow_clone` |
| No rebase in progress | `rebase_in_progress` |
| No merge in progress | `merge_in_progress` |
| Not detached HEAD | `detached_HEAD` |
| Has upstream branch | `no_upstream_branch` |
| Not diverged | `diverged_from_upstream` |

### Security Guardrails

**File Denylist** - Never committed regardless of agent output:

| Category | Patterns |
|----------|----------|
| **Secrets** | `.env`, `*.pem`, `*.key`, `id_rsa*`, `credentials.json` |
| **Build artifacts** | `node_modules`, `__pycache__`, `dist`, `build`, `target` |
| **Logs/temp** | `*.log`, `*.tmp`, `*.swp`, `.DS_Store` |
| **IDE files** | `.idea`, `.vscode`, `*.iml` |

**Secret Scanning:**

```bash
--secret-scan=none   # Disable
--secret-scan=warn   # Warn but continue (default)
--secret-scan=block  # Block push on detection
```

### Exit Codes

| Code | Meaning |
|------|---------|
| `0` | All repos processed successfully |
| `1` | Some repos failed (agent error, timeout) |
| `2` | Quality gate failures (secrets, tests) |
| `3` | System error (ntm, tmux missing) |
| `4` | Invalid arguments |
| `5` | Interrupted (use `--resume`) |

## Configuration

### XDG-Compliant Directory Structure

```
~/.config/ru/
├── config               # Main config file
└── repos.d/
    ├── public.list      # Public repos (one per line)
    └── private.list     # Private repos (gitignored)

~/.local/state/ru/
├── logs/
│   └── YYYY-MM-DD/
├── agent-sweep/
│   ├── state.json
│   └── results.ndjson
└── review/
    ├── digests/
    └── results/
```

### Repo List Format

```
# ~/.config/ru/repos.d/public.list
owner/repo
another-owner/another-repo@develop
private-org/repo@main as local-name
https://github.com/owner/repo.git
```

### Layout Modes

| Layout | Example Path |
|--------|--------------|
| `flat` | `/data/projects/repo` |
| `owner-repo` | `/data/projects/owner_repo` |
| `full` | `/data/projects/github.com/owner/repo` |

```bash
ru config --set LAYOUT=owner-repo
```

### Per-Repo Configuration

```yaml
# ~/.../your-repo/.ru-agent.yml
agent_sweep:
  enabled: true
  max_file_size: 5242880  # 5MB
  extra_context: "This is a Python project using FastAPI"
  pre_hook: "make lint"
  post_hook: "make test"
  denylist_extra:
    - "*.backup"
    - "internal/*"
```

## ntm Integration

When ntm (Named Tmux Manager) is available, RU uses its robot mode API:

| Function | Purpose |
|----------|---------|
| `ntm --robot-spawn` | Create Claude Code session in new tmux pane |
| `ntm --robot-send` | Send prompts with chunking for long messages |
| `ntm --robot-wait` | Block until session completes with timeout |
| `ntm --robot-activity` | Query real-time session state |
| `ntm --robot-status` | Get status of all managed sessions |
| `ntm --robot-interrupt` | Send Ctrl+C to interrupt long operations |

## Output Modes

### JSON Mode (`--json`)

```bash
ru sync --json 2>/dev/null
```

```json
{
  "version": "1.2.0",
  "timestamp": "2025-01-03T14:30:00Z",
  "summary": {
    "total": 47,
    "cloned": 8,
    "updated": 34,
    "current": 3,
    "conflicts": 2
  },
  "repos": [...]
}
```

### NDJSON Results Logging

```json
{"repo":"mcp_agent_mail","action":"pull","status":"updated","duration":2}
{"repo":"beads_viewer","action":"clone","status":"cloned","duration":5}
```

### jq Examples

```bash
# Get paths of all cloned repos
ru sync --json 2>/dev/null | jq -r '.repos[] | select(.action=="clone") | .path'

# Count by status
cat ~/.local/state/ru/logs/latest/results.ndjson | jq -s 'group_by(.status) | map({status: .[0].status, count: length})'
```

## Update Strategies

```bash
ru sync                        # Default: ff-only (safest)
ru sync --rebase               # Rebase local commits
ru sync --autostash            # Auto-stash before pull
ru sync --force                # Force update (use with caution)
```

| Strategy | Behavior |
|----------|----------|
| `ff-only` | Fast-forward only; fails if diverged |
| `rebase` | Rebase local commits on top of remote |
| `merge` | Create merge commit if needed |

## Quality Gates

Before applying changes, RU runs automated quality gates:

**Auto-detection by project type:**

| Project Type | Test Command | Lint Command |
|--------------|--------------|--------------|
| npm/yarn | `npm test` | `npm run lint` |
| Cargo (Rust) | `cargo test` | `cargo clippy` |
| Go | `go test ./...` | `golangci-lint run` |
| Python | `pytest` | `ruff check` |
| Makefile | `make test` | `make lint` |
| Shell scripts | (none) | `shellcheck *.sh` |

## Rate Limiting

RU includes an adaptive parallelism governor:

| Condition | Action |
|-----------|--------|
| GitHub remaining < 100 | Reduce parallelism to 1 |
| GitHub remaining < 500 | Reduce parallelism by 50% |
| Model 429 detected | Pause new sessions for 60s |
| Error rate > 50% | Open circuit breaker |

## Exit Codes (Sync)

| Code | Meaning |
|------|---------|
| `0` | Success - all repos synced or current |
| `1` | Partial failure - some repos failed |
| `2` | Conflicts exist |
| `3` | Dependency error (gh missing, auth failed) |
| `4` | Invalid arguments |
| `5` | Interrupted (use `--resume`) |

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RU_PROJECTS_DIR` | Base directory for repos | `/data/projects` |
| `RU_LAYOUT` | Path layout | `flat` |
| `RU_PARALLEL` | Parallel workers | `1` |
| `RU_TIMEOUT` | Network timeout (seconds) | `30` |
| `RU_UPDATE_STRATEGY` | Pull strategy | `ff-only` |
| `GH_TOKEN` | GitHub token | (from gh CLI) |

## Troubleshooting

### Common Issues

| Issue | Fix |
|-------|-----|
| `gh: command not found` | `brew install gh && gh auth login` |
| `gh: auth required` | `gh auth login` or set `GH_TOKEN` |
| `Cannot fast-forward` | Use `--rebase` or push first |
| `dirty working tree` | Commit changes or use `--autostash` |
| `diverged_from_upstream` | `git fetch && git rebase origin/main` |

### Debug Mode

```bash
# View latest run log
cat ~/.local/state/ru/logs/latest/run.log

# View specific repo log
cat ~/.local/state/ru/logs/latest/repos/mcp_agent_mail.log

# Run with verbose output
ru agent-sweep --verbose --debug
```

### Preflight Failure Debugging

```bash
# View why repos were skipped
ru agent-sweep --json 2>/dev/null | jq '.repos[] | select(.status == "skipped")'
```

## Installation

```bash
# One-liner
curl -fsSL https://raw.githubusercontent.com/Dicklesworthstone/repo_updater/main/install.sh | bash

# Verify
ru doctor
```

## Architecture Notes

- **~17,700 LOC** pure Bash, no external dependencies beyond git, curl, gh
- **Work-stealing queue** for parallel sync with atomic dequeue
- **Portable locking** via `mkdir` (works on all POSIX systems)
- **Path security validation** prevents traversal attacks
- **Retry with exponential backoff** for network operations

## Integration with Flywheel

| Tool | Integration |
|------|-------------|
| **Agent Mail** | Notify agents when repos are updated; coordinate reviews |
| **BV** | Track repo sync as recurring beads |
| **CASS** | Search past sync sessions and agent-sweep logs |
| **NTM** | Robot mode API for session orchestration |
| **DCG** | RU runs inside DCG sandbox protection |
