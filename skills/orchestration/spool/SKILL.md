---
name: spool
description: Unified entry point for spool commands with intelligent skill-first routing and CLI fallback.
---

Route spool commands to the best handler.

## Goal

Users may type requests like `spool archive 001-03_add-spool-skill` or `spool dashboard`.

This skill MUST:

1. Prefer matching spool-* skills (skill-first precedence)
2. Fall back to the spool CLI when no matching skill is installed
3. Preserve argument order and content

## Input

The requested command is provided either:

- As plain text following the word "spool" in the user request
- In prompt arguments (if your harness provides them)
- In a `<SpoolCommand>` block

## Steps

1. **Parse** the command:
   - Extract the primary command (first token) and the remaining args
   - If no command is provided, output a concise error: "Command is required" and show a one-line usage example

2. **Resolve skill target**:
   - Build candidate skill id: `spool-${command}`
   - Determine if that skill is installed/available in this harness
     - OpenCode: check for a directory under `.opencode/skills/`
     - Claude: check for a directory under `.claude/skills/`
     - GitHub Copilot: check for a directory under `.github/skills/`
     - Codex: skills are global; if unsure, assume not installed and use CLI fallback

3. **Execute**:
   - If matching skill exists: follow that skill's instructions, passing along the original args
   - Otherwise: invoke the CLI using Bash: `spool <command> <args...>`

4. **Error handling**:
   - If the invoked skill fails: prefix with `[spool-* skill error]` and preserve the original error
   - If the CLI fails: prefix with `[spool CLI error]` and preserve the original error
