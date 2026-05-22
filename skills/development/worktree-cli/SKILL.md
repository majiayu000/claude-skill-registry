---
name: worktree-cli
description: Git worktree management with worktree.py CLI. Use for creating worktrees, teardown, merging PRs, syncing branches, and Docker service management.
---

# worktree-cli Skill

**Auto-generated reference for `./worktree.py` commands.**

> This is the SOURCE OF TRUTH for worktree.py flags and options.
> Regenerate with: `.claude/scripts/generate-cli-docs.sh`

## When to Use This Skill

- Setting up new worktrees for issues
- Tearing down worktrees after PR merge
- Managing Docker services across worktrees
- Syncing worktrees after merges
- Troubleshooting worktree issues

## Quick Reference

| Command | Purpose | Key Flags |
|---------|---------|-----------|
| `setup <issue>` | Create worktree from GH issue | `--no-seed`, `--no-start`, `--build` |
| `complete <pr>` | **RECOMMENDED**: Full lifecycle completion | - |
| `teardown <name>` | Remove worktree only | `-f/--force`, `--keep-branch` |
| `list` | Show all worktrees | `-c/--compact` |
| `merge-pr <num>` | Merge PR + teardown | `--skip-sync`, `--skip-teardown` |
| `cleanup` | Remove merged branches | `-f/--force` (required to execute) |
| `logs` | View Docker logs | `-n <lines>`, `-f/--follow` |

**Prefer `complete` over `merge-pr`** - it handles issue closure and sync automatically.

## Common Workflows

### Start New Work
```bash
./worktree.py setup 42              # From issue number
cd ../42-feature-name
./worktree.py health                # Verify services
```

### Complete Work
```bash
# After PR created (orchestrator calls this):
./worktree.py complete 123          # Merge + close issue + sync + teardown
```

### Maintenance
```bash
./worktree.py cleanup               # Dry-run: show what would be cleaned
./worktree.py cleanup --force       # Actually clean up merged branches
./worktree.py prune                 # Remove stale registry entries
```

---

## Command Reference

### setup

Create a new git worktree with isolated Docker environment.

```
Usage: worktree.py setup [OPTIONS] ISSUE_OR_BRANCH

Arguments:
  ISSUE_OR_BRANCH  Issue number, branch name, or GitHub issue URL [required]

Options:
  --no-seed    Skip database seeding
  --no-start   Don't start Docker services after setup
  --build      Build Docker images before starting
  --help       Show this message and exit
```

**Examples:**
```bash
./worktree.py setup 42                              # From issue number
./worktree.py setup 42/feature-audio-analysis       # Explicit branch name
./worktree.py setup main                            # Register main worktree
./worktree.py setup https://github.com/.../issues/42  # From GitHub URL
```

---

### teardown

Remove a worktree and clean up all resources.

```
Usage: worktree.py teardown [OPTIONS] NAME_OR_BRANCH

Arguments:
  NAME_OR_BRANCH  Worktree name or branch to tear down [required]

Options:
  -f, --force      Force teardown even if branch not merged
  --keep-branch    Keep the git branch after teardown
  --help           Show this message and exit
```

**What it does:**
- Stops Docker containers
- Removes Docker volumes
- Deletes git worktree
- Optionally deletes branches (local and remote)

---

### list

List all registered worktrees with full details.

```
Usage: worktree.py list [OPTIONS]

Options:
  -c, --compact  Show compact table view
  --help         Show this message and exit
```

**Default:** Expanded view with containers, ports, and credentials.

---

### status

Show detailed status of current worktree.

```
Usage: worktree.py status [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### health

Check health of current worktree.

```
Usage: worktree.py health [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### ports

Show port allocations for all worktrees.

```
Usage: worktree.py ports [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### prune

Remove stale registry entries for non-existent worktrees.

```
Usage: worktree.py prune [OPTIONS]

Options:
  --help  Show this message and exit
```

**Note:** This command has NO `--force` flag. It runs immediately.
For cleaning merged branches, use `cleanup --force` instead.

---

### seed

Re-run database seeding from seed.sql.

```
Usage: worktree.py seed [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### start

Start Docker services for current worktree.

```
Usage: worktree.py start [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### stop

Stop Docker services for current worktree.

```
Usage: worktree.py stop [OPTIONS]

Options:
  --help  Show this message and exit
```

---

### sync

Sync all worktrees with main (fetch, update main, rebase feature branches).

```
Usage: worktree.py sync [OPTIONS]

Options:
  --help  Show this message and exit
```

**CRITICAL:** Run this after any PR is merged to prevent divergence.

---

### complete

**RECOMMENDED**: Complete a PR lifecycle atomically (merge + close issue + sync + teardown).

```
Usage: worktree.py complete PR_NUMBER

Arguments:
  PR_NUMBER  PR number to complete [required]
```

**What it does:**
1. Verifies/merges the PR (skips if already merged)
2. Closes the linked GitHub issue
3. Tears down the worktree (Docker, files, branch)

**Use this instead of `merge-pr`** for orchestrator-managed workflows.

---

### merge-pr

Merge a PR and sync worktrees (legacy - use `complete` instead).

```
Usage: worktree.py merge-pr [OPTIONS] PR_NUMBER

Arguments:
  PR_NUMBER  PR number to merge [required]

Options:
  --skip-sync      Skip syncing other worktrees
  --skip-teardown  Skip auto-teardown of merged worktree
  --help           Show this message and exit
```

**What it does:**
1. Checks if PR is already merged (handles gracefully if so)
2. Merges the PR via gh CLI (squash merge) if not yet merged
3. Auto-tears down the merged worktree (prevents rebase issues)
4. Updates main branch
5. Rebases all active feature worktrees onto new main

---

### validate

Validate environment and check for divergence.

```
Usage: worktree.py validate [OPTIONS]

Options:
  --help  Show this message and exit
```

**Performs comprehensive checks:**
- Git configuration
- Docker status
- Port allocations
- Main branch sync status
- Feature branch divergence

---

### cleanup

Clean up merged branches and orphaned Docker resources.

```
Usage: worktree.py cleanup [OPTIONS]

Options:
  -f, --force  Actually perform cleanup (default: dry-run)
  --help       Show this message and exit
```

**IMPORTANT:** By default runs in dry-run mode. Use `--force` to actually clean up.

---

### logs

Show Docker compose logs for current worktree.

```
Usage: worktree.py logs [OPTIONS]

Options:
  -n, --lines INTEGER  Number of lines to show [default: 50]
  -f, --follow         Follow log output
  --help               Show this message and exit
```

---

### hooks

Manage git hooks for automatic sync.

```
Usage: worktree.py hooks [OPTIONS] ACTION

Arguments:
  ACTION  Action: install, uninstall, or status [required]

Options:
  --help  Show this message and exit
```

**Actions:**
- `install` - Install post-commit hook for auto-sync
- `uninstall` - Remove post-commit hook
- `status` - Check if hooks are installed

**Disable auto-sync temporarily:**
```bash
GTS_NO_AUTO_SYNC=1 git commit -m "message"
```

---

### auth-status

Show auth status and token expiration.

```
Usage: worktree.py auth-status [OPTIONS]

Options:
  --help  Show this message and exit
```

**What it shows:**
- Whether T3K authentication is valid
- Username and expiration time
- Hours/days until expiration
- Path to auth file

---

### auth-login

Open browser to login via T3K OAuth.

```
Usage: worktree.py auth-login [OPTIONS]

Options:
  -p, --port INTEGER  Backend port for OAuth callback [default: 8000]
  --help              Show this message and exit
```

**What it does:**
- Opens browser to T3K OAuth page
- After login, tokens saved to shared auth file
- All worktrees can then use these credentials

**Example:**
```bash
./worktree.py auth-login --port 8030    # Use worktree's backend port
```

---

### auth-restore

Restore session from saved auth file.

```
Usage: worktree.py auth-restore [OPTIONS]

Options:
  -p, --port INTEGER  Backend port (auto-detected if not specified)
  --help              Show this message and exit
```

**What it does:**
- Reads T3K tokens from shared auth file
- Creates session in current worktree's backend
- Called automatically during `setup`

---

## Auth Workflow

**Initial authentication (once):**
```bash
./worktree.py setup 42              # Creates worktree
./worktree.py auth-login --port 8030  # Login via browser (uses worktree's backend)
```

**After that, all worktrees share the auth:**
```bash
./worktree.py setup 123             # Auto-restores auth from shared file
```

**Check status anytime:**
```bash
./worktree.py auth-status
```

---

## Common Mistakes to Avoid

| Wrong | Right | Why |
|-------|-------|-----|
| `prune --force` | `prune` | prune has no --force flag |
| `cleanup` alone | `cleanup --force` | cleanup is dry-run by default |
| `teardown` on main | Never teardown main | main is the base worktree |
| Manual `git pull` after merge | `merge-pr <num>` | merge-pr handles sync |
