---
name: allow-agent-commands
description: Add or change allowed commands in AI agent permission configs (OpenCode, Claude Code)
---

# Adding/Changing Allowed Commands

## When to use this skill

Use this skill when:

- A command needs to be added to the allow list for AI agents
- Permission settings need to be modified for existing commands
- Setting up a new AI tool that requires command permissions

## How it works

Commands must be explicitly allowed in the permission configs before agents
can run them. This skill covers adding entries to both OpenCode and Claude
Code configuration files.

**IMPORTANT**: The config files are stowed into `~` via GNU Stow symlinks.
Always edit them directly from within the ai-config repository, NOT from `~`.
The paths below are relative to the ai-config repository root.

## OpenCode Configuration

File: `.config/opencode/opencode.json` under `permission.bash`

Format:
```json
"uname *": "allow",
```

Pattern: `"command argpatterns": "action"` where `*` matches any args

**Important**: Insert new entries in alphabetical order by command name.
When adding a new command, find the correct position to maintain sorting.
**Do NOT reorder existing entries.**

## Claude Code Configuration

File: `.claude/settings.json` under `permissions.allow`

Format:
```json
"Bash(uname:*)",
```

**Important**: Insert new entries in alphabetical order. Commands are sorted
by the command name (the part after `Bash(` and before `:`).
**Do NOT reorder existing entries.**

## General Pattern for New AI Tools

When adding new AI tools:

1. Find their config file (usually in `~/.config/` or project root)
2. Look for `permissions`, `allowedCommands`, or similar sections
3. Add the command with glob patterns for arguments
4. **Insert new entries in alphabetical order by command name**
5. **Do NOT reorder existing entries.**

## After Adding Commands

After adding the new command entries to both config files:

1. Check if there are any other staged changes with `git status`
2. If there are NO other staged changes, stage ONLY the new hunks in the two
   config files using the `git-stager` subagent (be careful not to stage
   unrelated changes)
3. Invoke the `git-committer` subagent to commit the changes

## Examples

Adding `rg` (ripgrep) to both configs:

**OpenCode** (insert after `rev *`, before `rpm -q*`):
```json
"rg *": "allow",
```

**Claude Code** (insert after `Bash(rg:*)`, before `Bash(rpm -q:*)`):
```json
"Bash(rg:*)",
```
