---
name: claude-permissions-update
description: >
  Sync auto-approved permissions from all community-patterns directories
  (including community-patterns-2, -3, etc.) to the shared project settings.
  Shows new permissions for review before adding.
---

# Claude Permissions Update

**Use this skill to consolidate auto-approved permissions from all your community-patterns workspaces.**

## Overview

When you work across multiple community-patterns directories (e.g., community-patterns, community-patterns-2, etc.), you accumulate different auto-approved permissions in each directory's `.claude/settings.local.json`. This skill helps you:

1. Find all community-patterns directories
2. Gather all auto-approved permissions
3. Compare with the project-level `.claude/settings.json`
4. **Filter out junk and path-specific permissions automatically**
5. Show new permissions for your review by category
6. Let you select which to add to the shared settings

## Important: Local Settings Contain Junk

**WARNING:** The `settings.local.json` files often contain accidentally auto-approved garbage:
- Commit message fragments
- Shell script fragments like `Bash(do)`, `Bash(fi)`, `Bash(then ...)`
- Markdown content from heredocs
- Path-specific permissions like `Bash(../community-patterns-2/patterns/...)`

**The filtering step below is CRITICAL to avoid polluting project settings.**

## Step 1: Scan and Gather Permissions

```bash
# Find all community-patterns directories
echo "=== Scanning community-patterns directories ==="
for dir in /Users/alex/Code/community-patterns*; do
  echo "Found: $dir"
done
```

## Step 2: Extract and Filter New Permissions

```bash
# Get all local permissions (deduplicated)
ALL_LOCAL=$(for dir in /Users/alex/Code/community-patterns*; do
  jq -r '.permissions.allow[]?' "$dir/.claude/settings.local.json" 2>/dev/null
done | sort -u)

# Get project permissions
PROJECT_PERMS=$(jq -r '.permissions.allow[]?' .claude/settings.json 2>/dev/null | sort -u)

# Find new permissions - FILTER for valid patterns only
NEW_PERMS=$(comm -23 <(echo "$ALL_LOCAL") <(echo "$PROJECT_PERMS") | \
  grep -E '^(Bash\(|Skill\(|Read\(|WebFetch\(|mcp__|SlashCommand)')
```

## Step 3: Categorize for Review

**Present permissions in categories to help the user decide:**

### General Commands (with wildcards - usually worth syncing)
```bash
echo "=== General Bash commands (worth syncing) ==="
echo "$NEW_PERMS" | grep -E ':\*\)$' | grep -v '../community-patterns'
```

These have wildcards and are NOT path-specific. Good candidates to sync.

### WebFetch Domains
```bash
echo "=== WebFetch domains ==="
echo "$NEW_PERMS" | grep '^WebFetch'
```

### Skills and MCP Tools
```bash
echo "=== Skills ==="
echo "$NEW_PERMS" | grep '^Skill'

echo "=== MCP tools ==="
echo "$NEW_PERMS" | grep '^mcp__'
```

### Path-Specific (SKIP these)
```bash
echo "=== Path-specific permissions (SKIP) ==="
echo "$NEW_PERMS" | grep '../community-patterns'
```

These are specific to a particular checkout and should NOT be synced.

## Step 4: Review with User

**Use AskUserQuestion to walk through each category:**

1. Present general Bash commands one by one or in small groups
2. Present WebFetch domains (often safe to add all)
3. Present Skills and MCP tools
4. SKIP path-specific permissions automatically

**Ask about each permission individually or in logical groups.**

## Step 5: Update Project Settings

After user approval, edit `.claude/settings.json` to add the approved permissions to the `permissions.allow` array.

**Use the Edit tool** to add each permission as a new line in the array.

## Workflow Summary

1. **Scan** all community-patterns-* directories
2. **Extract** permissions from each `.claude/settings.local.json`
3. **Filter** - remove junk (non-permission strings) and validate format
4. **Compare** with `.claude/settings.json` to find new ones
5. **Categorize** - separate general vs path-specific
6. **Present** to user by category (skip path-specific automatically)
7. **Update** project settings with approved permissions
8. **Verify** JSON is valid with `jq . .claude/settings.json > /dev/null`

## What to Sync vs Skip

### SYNC These (General Permissions)
- `Bash(command:*)` - wildcarded commands
- `Bash(git subcmd:*)` - git subcommands
- `Bash(deno task:*)`, `Bash(timeout N command:*)` - tool commands
- `WebFetch(domain:example.com)` - domain-specific fetch
- `Skill(skill-name)` - skill invocations
- `mcp__server__tool` - MCP tool permissions
- `Read(//path/**)` - read patterns with wildcards

### SKIP These (Junk/Path-Specific)
- `Bash(../community-patterns-N/...)` - relative paths to specific checkouts
- `Bash(do)`, `Bash(fi)`, `Bash(then ...)` - shell fragments
- Anything that looks like a commit message or markdown
- Anything without parentheses or proper permission format

## Notes

- This skill does NOT modify the local settings files
- It only adds permissions to the shared project settings
- User must approve all additions
- After adding to project settings, the permissions will be available across all community-patterns workspaces
- Always verify JSON validity after editing
