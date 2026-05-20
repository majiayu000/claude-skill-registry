---
name: git-guardrails-claude-code
description: Install a Claude-Code PreToolUse hook that blocks destructive git commands (push variants including force-push, hard reset, force clean, branch -D, checkout/restore overwrites) before Bash runs them. Use when the user wants git safety rails, force-push prevention, or repository-wipe protection.
---

Bash-tool PreToolUse hook. The harness invokes the script with the candidate command on stdin as JSON; the script greps for dangerous patterns and exits non-zero with an explanatory stderr message, which the harness surfaces to the model as a refusal. The model cannot override the block.

## Blocked patterns (default)

- `git push` — all variants, including `--force` and `--force-with-lease`.
- `git reset --hard` — discards working tree and index irreversibly.
- `git clean -f` and `git clean -fd` — deletes untracked files and directories.
- `git branch -D` — force-deletes a branch, including unmerged work.
- `git checkout .` and `git restore .` — bulk-overwrites uncommitted changes.

## Install

### 1. Choose scope

- **Project-local** — `.claude/settings.json` and `.claude/hooks/block-dangerous-git.sh`. Travels with the repository.
- **Global** — `~/.claude/settings.json` and `~/.claude/hooks/block-dangerous-git.sh`. Applies to every project.

### 2. Place the hook script

Write the script (content below) to the chosen hooks directory. Mark executable with `chmod +x`.

### 3. Register the hook

Project (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-dangerous-git.sh"
          }
        ]
      }
    ]
  }
}
```

### 4. Verify

```bash
echo '{"tool_input":{"command":"git push origin main"}}' | /path/to/block-dangerous-git.sh
```

Expected: exit code 2, stderr contains `BLOCKED:`. A benign command (`git status`) must exit 0 with no output.

## Hook script (block-dangerous-git.sh)

```bash
#!/bin/bash

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

DANGEROUS_PATTERNS=(
  "git push"
  "git reset --hard"
  "git clean -fd"
  "git clean -f"
  "git branch -D"
  "git checkout \."
  "git restore \."
  "push --force"
  "reset --hard"
)

for pattern in "${DANGEROUS_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qE "$pattern"; then
    echo "BLOCKED: '$COMMAND' matches dangerous pattern '$pattern'. The user has prevented you from doing this." >&2
    exit 2
  fi
done

exit 0
```

Dependencies: `bash`, `jq`. The script is the contract surface; SKILL.md prescribes how to install and extend it.

## Cross-harness note

The hook concept generalises but the install surface differs:

- **Claude Code** — `PreToolUse` hook on the `Bash` matcher (this skill).
- **Codex CLI / Gemini CLI / other harnesses** — typically a wrapper around the shell-exec tool or an MCP-level guard. The script body (pattern list, exit-2 contract) ports unchanged; the registration JSON does not.
