---
name: issue
description: Use when user says "/issue", "create issue", "file issue", "report bug", "request feature", "update issue", "check off", "verify issue", "view issue", or needs to manage GitHub issues.
allowed-tools: Bash(gh:*), AskUserQuestion, Grep, Read, Edit, Write, TodoWrite
user-invocable: true
argument-hint: view <number> | verify <number> [--all] [--dry-run] | ralph-loop <number> [--max-iterations <n>] | scan [--milestone <name>] [--fix]
context: fork
---

# Issue Skill

Create, update, and manage GitHub issues following ZeroAE conventions. Infer as much as possible from context; only ask when ambiguous.

## Modes

| Mode | Trigger | Purpose |
|------|---------|---------|
| **View** | "view issue", "view #123", `/issue view <number>` | Display full issue details (body, criteria, deps, comments) |
| **Create** | "create issue", "file issue", "new issue", "report bug", "request feature" | Create new issue |
| **Update** | "update issue", "add to issue", "update #123" | Modify existing issue |
| **Progress** | "check off", "mark complete", "done with", "finished" | Check checkboxes based on work done |
| **Verify** | `/issue verify <number> [--all] [--dry-run]` | Validate unchecked criteria, prompt to check off |
| **Ralph Loop** | `/issue ralph-loop <number> [--max-iterations <n>]` | Iteratively work until all criteria pass |
| **Scan** | `/issue scan [--milestone <name>] [--fix]` | Flag subjective acceptance criteria |

## Mode Detection

When this skill is invoked, arguments follow the skill name (e.g., `/issue view 135` passes "view 135" as arguments).

**IMPORTANT:** Before doing anything else, identify the mode from the invocation arguments:

| Arguments | Mode | Instructions |
|-----------|------|--------------|
| `view <number>` | View | Read `view.md` |
| `ralph-loop <number>` | Ralph Loop | Read `ralph-loop.md` |
| `scan [--milestone <name>]` | Scan | Read `scan.md` |
| `verify <number>` | Verify | Read `verify.md` |
| update phrases ("update issue", "add to #123") | Update | Read `update.md` |
| progress phrases ("check off", "mark complete") | Progress | Read `progress.md` |
| (none) or create phrases | Create | Read `create.md` |

**First action:** Read the appropriate `.md` file for your detected mode, then follow those instructions exactly.

## Supported Issue Types

GitHub supports 5 issue types. The title emoji can be any gitmoji:

| GitHub Type | Canonical Emoji | Alternative Emojis | Use For |
|-------------|-----------------|-------------------|---------|
| Bug | 🐛 | 🔒 (security) | Defects, unexpected behavior |
| Feature | ✨ | ⚡ (perf), 💥 (breaking) | New functionality, enhancements |
| Task | 📋 | 📝 (docs), ✅ (test) | Documentation, testing, specific work items |
| Chore | 🔧 | ♻️ (refactor), ⬆️ (deps), 👷 (ci), 🔥 (remove) | Maintenance: refactor, deps, ci, cleanup |
| Epic | 🎯 | - | Major feature spanning multiple issues |
| Theme | 🎨 | - | Strategic initiative spanning epics |

See [conventions.md](conventions.md) for full gitmoji-to-type mapping.

> **Note:** For release preparation, use `/pr release <version>` to create a Release Prep PR.

## Reference Files

- [view.md](view.md) - View issue mode
- [create.md](create.md) - Create issue mode
- [update.md](update.md) - Update issue mode
- [progress.md](progress.md) - Progress tracking mode
- [verify.md](verify.md) - Acceptance criteria verification mode
- [ralph-loop.md](ralph-loop.md) - Ralph Loop mode (iterative issue resolution)
- [scan.md](scan.md) - Scan mode (flag subjective acceptance criteria)
- [templates.md](templates.md) - Issue body templates for each type
- [conventions.md](conventions.md) - Label taxonomy, title formatting, milestone rules
