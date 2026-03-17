---
name: git-worktree-setup
description: Set up Git worktrees for agent parallelization with isolated environments. Use when setting up parallel agent execution, creating isolated environments per agent, or enabling concurrent development workflows.
allowed-tools: Read, Grep, Glob
---

# Git Worktree Setup Skill

Guide creation of isolated Git worktree environments for parallel agent execution.

## When to Use

- Setting up parallel agent execution
- Creating isolated development environments
- Configuring port allocation for multiple instances
- Planning worktree directory structure

## Core Concepts

### Why Worktrees?

Git worktrees provide:

- Filesystem isolation per agent
- Shared Git object database
- Independent branches
- Clean checkout from origin/main

### Directory Structure

```text
repository_root/
├── trees/
│   ├── {adw_id}/           # Isolated worktree
│   │   ├── src/
│   │   ├── .ports.env
│   │   └── ...
│   └── ...                  # Up to 15 concurrent
├── agents/
│   └── {adw_id}/
│       └── adw_state.json
└── main codebase/
```

### Port Allocation

Deterministic formula:

```text
slot = hash(adw_id) % 15
backend_port = 9100 + slot
frontend_port = 9200 + slot
```

## Setup Workflow

### Step 1: Plan Worktree Location

Identify where worktrees should live:

```text
Default: trees/{adw_id}/
Alternative: .worktrees/{adw_id}/
```

### Step 2: Create Worktree

Commands to execute:

```bash
# Fetch latest
git fetch origin

# Create worktree with new branch
git worktree add trees/{adw_id} -b {branch_name} origin/main
```

### Step 3: Configure Ports

Create `.ports.env`:

```bash
BACKEND_PORT={backend_port}
FRONTEND_PORT={frontend_port}
VITE_BACKEND_URL=http://localhost:{backend_port}
```

### Step 4: Copy Environment

```bash
cp .env trees/{adw_id}/.env
cat trees/{adw_id}/.ports.env >> trees/{adw_id}/.env
```

### Step 5: Update Configurations

For any absolute path configurations (MCP, etc.):

- Update paths to point to worktree location
- Use absolute paths, not relative

### Step 6: Install Dependencies

```bash
cd trees/{adw_id}
# Backend dependencies
cd app/server && uv sync --all-extras
# Frontend dependencies
cd app/client && bun install
```

## Validation Checklist

After setup, validate:

- [ ] Worktree directory exists
- [ ] Git recognizes worktree (`git worktree list`)
- [ ] Branch is correct
- [ ] Ports are configured
- [ ] Environment files present
- [ ] Dependencies installed
- [ ] Application can start

## Cleanup Operations

### Remove Single Worktree

```bash
git worktree remove trees/{adw_id}
# Or force if uncommitted changes
git worktree remove trees/{adw_id} --force
```

### Prune Stale Worktrees

```bash
git worktree prune
```

### List All Worktrees

```bash
git worktree list
```

## Key Memory References

- @git-worktree-patterns.md - Full worktree documentation
- @adw-anatomy.md - ADW uses worktrees
- @zte-progression.md - ZTE requires parallelization

## Output Format

Provide setup plan:

```markdown
## Worktree Setup Plan

**ADW ID:** {adw_id}
**Branch Name:** {branch_name}
**Worktree Path:** trees/{adw_id}

### Port Allocation
- Backend: {backend_port}
- Frontend: {frontend_port}

### Commands to Execute
1. `git fetch origin`
2. `git worktree add trees/{adw_id} -b {branch_name} origin/main`
3. Create `.ports.env`
4. Copy and configure environment
5. Install dependencies

### Validation Steps
- [ ] Verify worktree created
- [ ] Test port availability
- [ ] Confirm dependencies installed
```

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Worktree already exists | Remove first or use different ID |
| Port in use | Check what's using it, kill or use different |
| Branch exists | Use existing branch or delete first |
| Permission denied | Check directory permissions |

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
