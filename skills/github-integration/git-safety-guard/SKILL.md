---
name: git-safety-guard
description: |
  Blocks destructive git and filesystem commands before execution.
  Prevents accidental loss of uncommitted work from git checkout --,
  git reset --hard, rm -rf, and similar destructive operations.
  Works as a Claude Code PreToolUse hook with fail-open semantics.
license: Apache-2.0
---

# Git Safety Guard

Use this skill when setting up or configuring protection against destructive git/filesystem commands in Claude Code.

## Overview

Git Safety Guard intercepts Bash commands before execution and blocks dangerous operations that could permanently destroy uncommitted work or important files. The guard uses regex pattern matching with an allowlist to distinguish between safe and dangerous variants of commands.

**Key Features:**
- `terraphim-agent guard` - CLI command for pattern checking
- PreToolUse hook - Intercept Claude Code tool calls before execution
- Allowlist support - Safe patterns override dangerous patterns
- Fail-open semantics - If guard fails, commands pass through

## Architecture

```
Claude Code PreToolUse
      |
      v
git_safety_guard.sh (shell wrapper)
      |
      v
terraphim-agent guard --json "$COMMAND"
      |
      v
Pattern Matching (Regex)
      |
      +---> SAFE_PATTERNS (allowlist) -> Allow
      |
      +---> DESTRUCTIVE_PATTERNS -> Block with reason
      |
      +---> No match -> Allow
```

## Commands Blocked

| Command Pattern | Reason |
|-----------------|--------|
| `git checkout -- <files>` | Discards uncommitted changes permanently |
| `git restore <files>` | Discards uncommitted changes (except --staged) |
| `git reset --hard` | Destroys all uncommitted changes |
| `git reset --merge` | Can lose uncommitted changes |
| `git clean -f` | Removes untracked files permanently |
| `git push --force` | Destroys remote history |
| `git push -f` | Same as --force |
| `git branch -D` | Force-deletes branch without merge check |
| `rm -rf` (non-temp paths) | Recursive file deletion |
| `git stash drop` | Permanently deletes stashed changes |
| `git stash clear` | Deletes ALL stashed changes |
| `git commit --no-verify` | Bypasses pre-commit and commit-msg hooks |
| `git commit -n` | Same as --no-verify |
| `git push --no-verify` | Bypasses pre-push hooks |

## Commands Explicitly Allowed

| Command Pattern | Why Safe |
|-----------------|----------|
| `git checkout -b <branch>` | Creates new branch, doesn't modify files |
| `git checkout --orphan` | Creates orphan branch |
| `git restore --staged` | Only unstages files, doesn't discard changes |
| `git clean -n` / `--dry-run` | Preview only, no actual deletion |
| `git push --force-with-lease` | Safer force push with remote check |
| `rm -rf /tmp/...` | Temp directories are designed for ephemeral data |
| `rm -rf /var/tmp/...` | System temp directory |
| `rm -rf $TMPDIR/...` | User's temp directory |

## For Humans

### Quick Start

```bash
# Install terraphim-agent from GitHub releases (latest version)
# macOS ARM64 (Apple Silicon)
gh release download --repo terraphim/terraphim-ai \
  --pattern "terraphim-agent-aarch64-apple-darwin" --dir /tmp
chmod +x /tmp/terraphim-agent-aarch64-apple-darwin
mv /tmp/terraphim-agent-aarch64-apple-darwin ~/.cargo/bin/terraphim-agent

# macOS x86_64 (Intel)
# gh release download --repo terraphim/terraphim-ai \
#   --pattern "terraphim-agent-x86_64-apple-darwin" --dir /tmp

# Linux x86_64
# gh release download --repo terraphim/terraphim-ai \
#   --pattern "terraphim-agent-x86_64-unknown-linux-gnu" --dir /tmp

# Note: crates.io version (cargo install terraphim_agent) is outdated (v1.0.0)
# and missing the guard command. Use GitHub releases for latest features.

# Test guard command
echo "git checkout -- file.txt" | terraphim-agent guard --json
# Output: {"decision":"block","reason":"git checkout -- discards...","command":"..."}

echo "git checkout -b new-branch" | terraphim-agent guard --json
# Output: {"decision":"allow","command":"git checkout -b new-branch"}
```

### Installation

**Project-local installation:**
```bash
# Copy hook script
cp .claude/hooks/git_safety_guard.sh /your/project/.claude/hooks/

# Add to .claude/settings.local.json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": ".claude/hooks/git_safety_guard.sh"
      }]
    }]
  }
}
```

**Global installation (~/.claude/):**
```bash
# Run install script with --global flag
./scripts/install-terraphim-hooks.sh --global
```

### CLI Usage

```bash
# Check a command (JSON output)
echo "git reset --hard" | terraphim-agent guard --json

# Check a command (human output - exits with code 1 if blocked)
echo "rm -rf /home/user" | terraphim-agent guard

# Fail-open mode (always exit 0)
echo "git checkout -- ." | terraphim-agent guard --fail-open
```

## For AI Agents

### Detecting Guard Availability

```bash
# Check if terraphim-agent is available
if command -v terraphim-agent >/dev/null 2>&1; then
    echo "Guard available"
elif [ -x "./target/release/terraphim-agent" ]; then
    AGENT="./target/release/terraphim-agent"
fi
```

### Using Guard in Hooks

**PreToolUse Hook Pattern:**

```bash
#!/bin/bash
# Read JSON input
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

# Only process Bash commands
[ "$TOOL_NAME" != "Bash" ] && exit 0

# Check command
RESULT=$(terraphim-agent guard --json <<< "$COMMAND")

# If blocked, output deny decision
if echo "$RESULT" | jq -e '.decision == "block"' >/dev/null; then
    REASON=$(echo "$RESULT" | jq -r '.reason')
    cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "BLOCKED: $REASON"
  }
}
EOF
fi

exit 0
```

### Guard Response Format

**Blocked command:**
```json
{
  "decision": "block",
  "reason": "git checkout -- discards uncommitted changes permanently. Use 'git stash' first.",
  "command": "git checkout -- file.txt",
  "pattern": "git\\s+checkout\\s+--\\s+"
}
```

**Allowed command:**
```json
{
  "decision": "allow",
  "command": "git checkout -b new-branch"
}
```

## Error Handling

The guard uses **fail-open** semantics:
- If terraphim-agent is not found: pass through unchanged
- If pattern matching fails: allow command
- Errors logged to stderr only in verbose mode

Enable verbose mode:
```bash
export TERRAPHIM_VERBOSE=1
```

## What Happens When Blocked

When Claude tries to run a blocked command, it receives feedback like:

```
BLOCKED by git_safety_guard

Reason: git checkout -- discards uncommitted changes permanently. Use 'git stash' first.

Command: git checkout -- file.txt

If this operation is truly needed, ask the user for explicit permission and have them run the command manually.
```

The command never executes. Claude sees this feedback and should ask the user for help.

## Testing

```bash
# Manual test - should be blocked
echo "git checkout -- test.txt" | terraphim-agent guard --json

# Manual test - should be allowed
echo "git checkout -b feature" | terraphim-agent guard --json

# Run unit tests
cargo test -p terraphim_agent guard_patterns

# Test hook script
echo '{"tool_name":"Bash","tool_input":{"command":"git reset --hard"}}' | \
  .claude/hooks/git_safety_guard.sh
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Hook not triggering | Check `.claude/settings.local.json` configuration |
| Command not blocked | Verify pattern matches with `terraphim-agent guard --json` |
| Agent not found | Build with `cargo build -p terraphim_agent --release` |
| Permission denied | Run `chmod +x .claude/hooks/git_safety_guard.sh` |
| jq not found | Install jq: `brew install jq` or `apt install jq` |

## The Incident That Prompted This

On December 17, 2025, an AI agent ran `git checkout --` on multiple files containing hours of uncommitted work from another agent. This destroyed the work instantly and silently. The files were recovered from a dangling Git object via `git fsck --lost-found`, but it was a close call.

**Instructions alone don't prevent accidents. Mechanical enforcement does.**

## Related Skills

- `terraphim-hooks` - Knowledge graph-based text replacement
- `implementation` - For building custom guards
- `testing` - For validating guard behavior
- `devops` - For CI/CD integration with hooks
