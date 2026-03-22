---
name: analyze-permissions
description: Use when Claude Code permissions have accumulated in settings.local.json and you want to audit, consolidate, or clean up tool permission patterns.
effort: medium
argument-hint: "[analyze|apply|cleanup]"
disable-model-invocation: True
---


# Analyze Permissions

## Purpose

Analyze accumulated permissions in `settings.local.json` and suggest smart wildcard patterns to consolidate into shared configuration. Reduces permission sprawl by replacing specific entries with safe wildcard patterns.

## Arguments (parsed from user input)

- **action**: What to do - `analyze` (default), `apply`, or `cleanup`

Example invocations:

- `/ai-analyze-permissions` → analyze and suggest patterns
- `/ai-analyze-permissions apply` → apply suggested patterns to shared config
- `/ai-analyze-permissions cleanup` → just run the cleanup script

## Process

### Step 1: Read Current Permissions

Read these files:

1. **Project-local**: `<project-root>/.claude/settings.local.json` - accumulated "Always allow" permissions (per-project)
2. **Global**: `~/.claude/settings.json` - shared/base permissions across all projects

Note: `settings.local.json` is project-specific. Each repo has its own at `<repo>/.claude/settings.local.json`. The global `~/.claude/settings.json` is shared across all projects.

### Step 2: Analyze Patterns

For each entry in `settings.local.json`:

1. **Check if already covered** - Is there a wildcard in `settings.json` that covers this?
   - `Bash(git commit -m "Fix bug")` is covered by `Bash(git commit:*)`
   - `Bash(curl https://api.example.com)` is covered by `Bash(curl:*)`

2. **Identify pattern opportunities** - Group similar commands:
   - Multiple `kubectl` commands → suggest `Bash(kubectl:*)`
   - Multiple `docker` commands → suggest `Bash(docker:*)`
   - Multiple WebFetch for same domain → suggest `WebFetch(https://example.com/*)`

3. **Decide global vs local** - Where should the pattern live?
   - **Global (`~/.claude/settings.json`)**: General-purpose tools used across projects (`npx`, `python`, `docker compose`, etc.)
   - **Local (`settings.local.json`)**: Project-specific commands, or write operations you only want for that project (e.g., `git push` for a personal repo)

4. **Assess safety** - Consider if the pattern is safe for auto-approval:
   - Read-only commands: Generally safe
   - Commands with side effects: Flag for review
   - Overly broad patterns: Warn about security implications

### Step 3: Present Analysis

Output a structured report:

```markdown
## Permission Analysis

### Settings Overview
- settings.local.json: X entries
- settings.json: Y entries (Z wildcards)

### Already Covered (can be removed)
These entries in settings.local.json are redundant:

| Entry | Covered by |
|-------|------------|
| Bash(git commit -m "...") | Bash(git commit:*) |

### Suggested New Patterns
These patterns would consolidate multiple specific entries:

| Pattern | Covers | Scope | Safety |
|---------|--------|-------|--------|
| Bash(kubectl:*) | 4 entries | global | Safe (read-heavy) |
| Bash(docker exec:*) | 3 entries | local | Review (can modify) |

### Uncategorized
These entries don't fit a pattern (one-offs):

- Bash(some-specific-command)
```

### Step 4: Handle Actions

Based on the action argument:

**analyze (default):**

- Present the report
- Ask if user wants to apply suggestions

**apply:**

- For each suggested pattern, ask for confirmation
- Add approved global patterns to `~/.claude/settings.json` by editing the `permissions.allow` array
- Add approved local patterns to `<project-root>/.claude/settings.json` (project-level, not local)
- Run the cleanup script to remove now-redundant entries from `settings.local.json`

**cleanup:**

- Run `<project-root>/.claude/skills/ai-analyze-permissions/scripts/cleanup-settings-local.sh`

### Step 5: Apply Patterns (if applying)

When adding patterns:

1. Read the target settings file (`~/.claude/settings.json` for global, `<project-root>/.claude/settings.json` for project)
2. Add new entries to the `permissions.allow` JSON array
3. Write the updated JSON back (preserving all other fields)
4. Run cleanup to remove now-redundant entries: `<project-root>/.claude/skills/ai-analyze-permissions/scripts/cleanup-settings-local.sh`

**Important**: Adding patterns to `settings.json` never removes existing entries. The cleanup script only cleans `settings.local.json`. To clean `settings.json` itself, manually remove redundant entries.

## Pattern Safety Guidelines

**Safe to auto-approve (commonly needed):**

- `Bash(npx:*)`, `Bash(node:*)`, `Bash(npm:*)`, `Bash(pnpm:*)` - JS/Node tooling
- `Bash(python:*)`, `Bash(python3:*)`, `Bash(pip:*)` - Python tooling
- `Bash(cargo :*)`, `Bash(cd :* && cargo:*)` - Rust tooling
- `Bash(docker compose:*)`, `Bash(docker ps:*)` - Docker
- `Bash(kubectl get:*)`, `Bash(kubectl describe:*)` - K8s read operations
- `Bash(git:*)` subcommands (add, commit, log, diff, etc.)
- `Bash(gh:*)` read operations (pr view, issue list, api, etc.)
- `Bash(chmod:*)`, `Bash(ln:*)`, `Bash(wc:*)`, `Bash(which:*)` - basic utilities
- `Bash(ssh:*)`, `Bash(tmux:*)`, `Bash(bash:*)`, `Bash(zsh:*)` - shell/system
- `WebFetch(domain:*)`, `WebSearch` - web access

**Require review (side effects):**

- `Bash(kubectl delete:*)`, `Bash(kubectl apply:*)`
- `Bash(docker rm:*)`, `Bash(docker exec:*)`
- `Bash(aws s3 rm:*)`
- `Bash(rm:*)`, `Bash(mv:*)`
- `Bash(git push:*)` - consider keeping per-project in local settings

**Never auto-approve:**

- `Bash(sudo:*)`
- `Bash(chmod 777:*)`
- Patterns that could leak secrets

$ARGUMENTS
