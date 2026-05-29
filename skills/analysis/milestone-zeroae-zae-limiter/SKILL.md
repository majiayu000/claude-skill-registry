---
description: When users mention a milestone version (e.g., "0.4.0", "v0.4.0") or ask about release status, invoke this skill to analyze GitHub milestone progress, issues, and suggest next steps.
argument-hint: [version] | list
allowed-tools: Bash(gh api:*), Bash(gh issue list:*), Bash(gh issue view:*)
context: fork
model: haiku
---

# Milestone Skill

Analyze and summarize GitHub milestone status for this repository.

## Arguments

- `$ARGUMENTS`: One of:
  - `<version>` - Analyze a specific milestone (e.g., "v0.4.0" or "0.4.0")
  - `list` - List all open milestones
  - (empty) - List all open milestones

## Subcommand Instructions

Each subcommand has detailed instructions in a separate file:

| Command | Instructions |
|---------|--------------|
| `list` or empty | See `list.md` |
| `<version>` | See `status.md` |

Read the appropriate file based on the argument, then follow its instructions.
