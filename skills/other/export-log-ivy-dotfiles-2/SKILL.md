---
name: export-log
description: Export Claude conversation logs to markdown
argument-hint: "[CONVERSATION...]"
disable-model-invocation: true
context: fork
allowed-tools: Bash(claude-extract:*), Grep, Read
---

# Export Claude Conversation Logs

Export conversations using `claude-conversation-extractor`.

## Current Session

Session ID: `${CLAUDE_SESSION_ID}`

## Arguments

$ARGUMENTS

## Instructions

Parse the arguments and determine the export method:

### No arguments (export current session)

1. Run `claude-extract --list 2>/dev/null | grep -B5 "${CLAUDE_SESSION_ID:0:8}"` to find the session number
2. Extract the session number from the output (e.g., "17. " means session 17)
3. Run `claude-extract --extract <number> --detailed`

### Numeric arguments (session numbers)

If arguments are comma-separated numbers like `1`, `1,3,5`:
- Run `claude-extract --extract <numbers> --detailed`

### UUID-like arguments (session ID prefixes)

If arguments look like hex strings (e.g., `97b86784`, `14b9611d-cd1a`):
1. For each ID prefix, run `claude-extract --list 2>/dev/null | grep -B5 "<prefix>"` to find the session number
2. Collect all session numbers
3. Run `claude-extract --extract <numbers> --detailed`

### Text arguments (search)

If arguments are freeform text:
- Run `claude-extract --search "<text>"`

## Output

Report the exported file path(s) and message count to the user.

## Help

If unsure about available options, run `claude-extract --help`.
