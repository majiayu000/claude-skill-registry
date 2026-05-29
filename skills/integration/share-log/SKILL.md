---
name: share-log
description: Use when sharing the current conversation as a Gist. Creates a private Gist with the session log.
argument-hint: "[description for filename]"
{{- template "bedrock-model" (dict "tier" "haiku" "root" .) }}
allowed-tools:
  - Bash(~/.claude/skills/share-log/claude-extract-session:*)
  - Bash(gh gist create:*)
---

# Share Conversation Log

Creates a private Gist containing the current Claude Code conversation.

## Arguments

```
$ARGUMENTS
```

Optional description to include in the Gist filename. Defaults to "conversation".

## Instructions

### 1. Determine Filename

Use the argument if provided, otherwise default to "conversation":

```
claude-conversation-<description>.md
```

Sanitize the description: lowercase, replace spaces with hyphens, keep only alphanumeric and hyphens.

### 2. Extract Session and Create Gist

Extract **only the current session** and pipe directly to a secret Gist:

```bash
~/.claude/skills/share-log/claude-extract-session "${CLAUDE_SESSION_ID}" \
  | gh gist create --filename "claude-conversation-<description>.md" -
```

The shim:
- Takes the current session ID (provided by the `${CLAUDE_SESSION_ID}` substitution)
- Extracts **only that session** with `--detailed` output
- Writes markdown to stdout (no files created on disk)
- Pipes directly to `gh gist create` (secret by default)

### 3. Report Result

Output the Gist URL to the user. The Gist is secret (not listed publicly, but accessible via URL).

## Examples

```
/share-log                          -> claude-conversation-conversation.md
/share-log debugging auth issue     -> claude-conversation-debugging-auth-issue.md
/share-log refactoring-session      -> claude-conversation-refactoring-session.md
```

## Edge Cases

- **No session ID:** Error - `${CLAUDE_SESSION_ID}` should always be available
- **gh not authenticated:** Prompt user to run `gh auth login`
- **claude-extract not installed:** Direct user to install it
