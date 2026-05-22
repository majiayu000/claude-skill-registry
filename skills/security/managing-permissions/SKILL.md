---
name: managing-permissions
description: |-
  Guide for configuring Claude Code permissions in settings.json with security
  best practices for allow, ask, and deny rules. Use when: (1) Setting up or
  modifying permissions in settings.json, (2) Discussing tool permissions, access
  control, or security configuration, (3) User mentions allowing, blocking, or
  restricting specific tools or file access, (4) Configuring Bash command
  permissions, file access (Read/Edit/Write), or WebFetch restrictions, (5)
  Questions about what permissions are safe vs risky, (6) Troubleshooting
  permission-related errors or "permission denied" issues, (7) Reviewing
  security configuration or hardening Claude Code access.
---

# Managing Permissions

Configure Claude Code permissions to control tool access and protect sensitive files.

## Overview

Permissions are configured in `settings.json` using three groups: **allow**, **ask**, and **deny**.

**Rule precedence**: Deny > Ask > Allow

**Configuration hierarchy** (highest to lowest):

1. Managed settings (enterprise policies)
1. Command-line arguments
1. Local project settings (`.claude/settings.local.json`)
1. Shared project settings (`.claude/settings.json`)
1. User global settings (`~/.claude/settings.json`)

## Permission Groups

### Allow

Grants explicit permission for tool use without confirmation.

**When to use:** Safe, routine operations that don't risk data loss or security exposure.

**Examples:** Reading source code, running tests, read-only git commands.

See **[references/allow-permissions.md](references/allow-permissions.md)** for guidance and examples.

### Ask

Prompts for user confirmation before allowing tool use.

**When to use:** Operations requiring review, such as publishing changes or modifying dependencies.

**Examples:** Git push/commit, package installation, editing critical config files.

See **[references/ask-permissions.md](references/ask-permissions.md)** for examples and avoiding permission fatigue.

### Deny

Explicitly blocks tool use. Takes precedence over allow and ask rules.

**⚠️ Important:** Deny rules are workflow controls, NOT security mechanisms. They have significant limitations (tool-specific, easily bypassed, prefix-only matching for Bash).

**When to use:**

- Resource management (blocking node_modules, build artifacts to save tokens)
- Workflow guardrails (preventing accidental git push to main)
- Focus management (avoiding deprecated/legacy code)

**NOT for security:** For protecting secrets and credentials, use hooks instead (PreToolUse hooks provide tool-agnostic protection).

See **[references/deny-permissions.md](references/deny-permissions.md)** for key limitations and proper use cases.

## Basic Syntax

All permission rules follow this format:

```
ToolName(pattern)
```

**Available Tools:** Bash, Read, Edit, Write, Glob, Grep, WebFetch, WebSearch, NotebookEdit, Task, Skill, SlashCommand, TodoWrite, AskUserQuestion, BashOutput, KillShell, ExitPlanMode

**Most common:** Bash, Read, Edit, Write, Glob, Grep, WebFetch

**Pattern types:**

- **Bash**: Prefix matching - `Bash(git status)` matches "git status", "git status file.txt"
- **File tools**: Glob matching - `Read(src/**)` matches all files in src/ recursively

**Important:** Bash patterns use prefix-only matching and can be bypassed with command chaining. See deny-permissions.md for complete limitations.

See **[references/official-reference.md](references/official-reference.md)** for complete syntax reference and known limitations.

## Configuration Workflow

When setting up permissions:

1. **For security: Use hooks** - Protect secrets with PreToolUse hooks (deny rules aren't sufficient for security)
1. **Add deny rules** - Block large files (node_modules, build artifacts) to save tokens, prevent workflow mistakes
1. **Add allow rules** - Enable routine safe operations
1. **Add ask rules** - Require confirmation for important operations
1. **Test configuration** - Verify typical workflows work correctly
1. **Iterate** - Add rules as needed based on actual usage

## Getting Started

**For security:** Use PreToolUse hooks to protect secrets and credentials (see Claude Code documentation on hooks).

**Sample workflow configuration:**

```json
{
  "permissions": {
    "deny": [
      // Resource management (save tokens)
      "Read(node_modules/**)",
      "Read(build/**)",
      "Read(dist/**)",
      "Read(*.min.js)",

      // Workflow guardrails (prevent mistakes)
      "Bash(git push origin main:*)",
      "Bash(npm publish:*)"
    ],
    "allow": [
      "Bash(bun run test:*)",
      "Bash(git status)",
      "Bash(git diff:*)",
      "Read(src/**)",
      "Read(tests/**)"
    ],
    "ask": [
      "Bash(git push:*)",
      "Bash(bun install:*)"
    ]
  }
}
```

**Note:** Hooks handle security (secrets, credentials). Deny rules handle workflow controls.

## Reference Files

Concise guides with practical examples:

- **[references/allow-permissions.md](references/allow-permissions.md)** - What to allow (non-destructive, reversible operations), practical examples, key principles
- **[references/ask-permissions.md](references/ask-permissions.md)** - What to ask for (external changes, dependencies, critical configs), avoiding permission fatigue
- **[references/deny-permissions.md](references/deny-permissions.md)** - Key limitations (tool-specific), proper use cases (resource management, workflow guardrails), why hooks are needed for security
- **[references/layering-permissions.md](references/layering-permissions.md)** - Strategic permission layering (broad allow + narrow ask/deny), how precedence enables maintainable configurations, critical warning about build tools
- **[references/git-permissions.md](references/git-permissions.md)** - Git-specific permission patterns, security implications of git commands
- **[references/build-tool-permissions.md](references/build-tool-permissions.md)** - Recommended configuration patterns for build tools (npm, gradle, maven, make, cargo, etc.), core principles, decision framework
- **[references/official-reference.md](references/official-reference.md)** - Complete technical reference, glob syntax, known limitations
