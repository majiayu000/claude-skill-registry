---
name: create-worktree-skill
description: Use when the user explicitly asks for a SKILL to create a worktree. If the user does not mention "skill" or explicitly request skill invocation, do NOT trigger this. Only use when user says things like "use a skill to create a worktree" or "invoke the worktree skill". Creates isolated git worktrees with parallel-running configuration.
allowed-tools: SlashCommand, Bash, Read, Write, Edit, Glob, Grep
---

# Worktree Creator Skill

This skill enables creating fully configured git worktrees for parallel development with isolated ports, databases, and configuration.

## When to use this skill

Use this skill when:
- User asks to create a git worktree
- User wants to set up parallel development environments
- User needs to run multiple instances simultaneously
- User mentions working on multiple branches at once
- User wants isolated testing environments

## Instructions

### Step 1: Understand the request

Extract from the user's request:
- **Branch name** (required): The git branch to create the worktree from
  - If the branch name is not provided, stop and ask the user to provide a branch name
- **Port offset** (optional): Custom port offset (if not provided, auto-calculated)

### Step 2: Invoke the slash command

Use the SlashCommand tool to run:

```
/create_worktree_prompt <branch-name> [port-offset]
```

**Examples:**
- `/create_worktree_prompt feature-auth` - Creates worktree with auto-calculated ports
- `/create_worktree_prompt fix-bug 2` - Creates worktree with port offset 2 (ports 4020, 5193)

### Step 3: Share results

The `/create_worktree_prompt` command will:
- Create the git worktree in `trees/<branch-name>`
- Configure isolated ports (auto-incremented to avoid conflicts)
- Set up environment files with proper configuration
- Install dependencies for server and client
- Start both services automatically
- Provide access URLs and management instructions

Share the command output with the user, highlighting:
- Access URLs for the dashboard
- Ports being used
- How to stop/restart the worktree
- How to remove it later

## Examples

### Example 1: Simple worktree creation

**User:** "Create a worktree for the feature-dashboard branch"

**Your response:** Use SlashCommand to run `/create_worktree_prompt feature-dashboard`

### Example 2: Worktree with specific port offset

**User:** "Set up a parallel environment on branch hotfix-security with port offset 5"

**Your response:** Use SlashCommand to run `/create_worktree_prompt hotfix-security 5`

### Example 3: Multiple worktrees

**User:** "I need worktrees for branches: feature-a, feature-b, and feature-c"

**Your response:**
1. Use SlashCommand to run `/create_worktree_prompt feature-a`
2. Use SlashCommand to run `/create_worktree_prompt feature-b`
3. Use SlashCommand to run `/create_worktree_prompt feature-c`

Each will automatically get unique ports (4010/5183, 4020/5193, 4030/5203).

## Related capabilities

- The created worktree will run automatically with isolated ports, database, and configuration
- Each worktree is completely independent and can run simultaneously with others

## Troubleshooting

If the command fails, common issues:
- Branch name already exists as a worktree
- Ports are in use (command kills them automatically)
- Missing dependencies (ensure bun is installed)
- Git worktree errors (handle uncommitted changes first)

The slash command provides detailed error messages and suggestions.
